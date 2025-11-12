from tmp.prefilter import prefilter
from tmp.capture import capture
from tmp.analysis import analyze_input
from tmp.spectral_weighting import compute_weight
from tmp.bifurcation import decide_branch
from tmp.reports import daily_report
from tmp.policy import Policy
from persistent.clusters import PersistentMemory
from persistent.store_hdf5 import H5Store
from persistent.journal import Journal

from utils.color_os import color_tag
from utils.tensors import encode_tensor_scalar
from tmp.heuristics import Heuristics

class Orchestrator:
    def _heur(self):
        if not hasattr(self, '__heur'): self.__heur = Heuristics()
        return self.__heur

    def __init__(self):
        self.tmp_memory=[]
        self.mem=PersistentMemory()
        self.h5=H5Store()
        self.journal=Journal()
        self.policy=Policy()
    def process_input(self, data, user_subjective=0.0, self_subjective=0.0, user_save_override=False, system_save_override=False):
        raw=prefilter(data)
        cap = capture(raw)
        if raw is None:
            self.journal.log('drop', {'reason':'empty'})
            return {'status':'dropped'}
        feats=analyze_input(raw)
        entry={'data':raw,'capture':cap,'features':feats}
        # blockers (immutable / safety / policy) -> BLOCKED
        blocked, reason = self._heur().check_blockers(raw)
        if blocked:
            self.journal.log('blocked', {'reason': reason, 'data': raw})
            return {'status':'BLOCKED','reason':reason}

        # WTF if ambiguity high (very low tokens)
        tokens = feats.get('C',{}).get('tokens', 0)
        if tokens < 2 and not (user_save_override or system_save_override):
            self.journal.log('wtf', {'data': raw, 'tokens': tokens})
            return {'status': 'WTF', 'question': 'Please clarify context.'}

        w, G, M, ctx = compute_weight(entry,feats,user_subjective,self_subjective,self.policy)
        entry['weight']=w
        entry['G']=G; entry['M']=M

        # overrides: user/system can force save to MEM
        if user_save_override or system_save_override:
            sym=feats.get('M',{}).get('symbol','default')
            it=feats.get('M',{}).get('intent','general')
            ct = color_tag(M); ctag, cint = ct['tag'], ct['intensity']
            table={
                'Lp': len(self.mem.clusters.get(sym, type('x',(),{'entries':[]})).entries)+1 if hasattr(self.mem,'clusters') else 1,
                'Ref': str(uuid.uuid4()),
                'Date': __import__('datetime').datetime.utcnow().isoformat(),
                'Context': feats.get('T',{}).get('type',''),
                'Links': [],
                'G': float(G),
                'M': float(M),
                'ColorOS': {'tag': ctag, 'intensity': cint}
            }
            tensor = encode_tensor_scalar(w, G, M, tokens)
            saved=self.mem.store(sym,it,tensor,metadata={'data':raw}, table=table)
            self.h5.append(sym,it,tensor)
            self.journal.log('mem_store_override', {'symbol':sym,'intent':it,'weight':w,'override':'user' if user_save_override else 'system'})
            return {'status':'MEM','saved':saved,'override':True}

        branch=decide_branch(w)
        if branch=='mem':
            sym=feats.get('M',{}).get('symbol','default')
            it=feats.get('M',{}).get('intent','general')
            ct = color_tag(M); ctag, cint = ct['tag'], ct['intensity']
            table={'Lp': len(self.mem.clusters.get(sym, type('x',(),{'entries':[]})).entries)+1 if hasattr(self.mem,'clusters') else 1,
                   'Ref': str(uuid.uuid4()), 'Date': __import__('datetime').datetime.utcnow().isoformat(),
                   'Context': feats.get('T',{}).get('type',''), 'Links': [], 'G': float(G), 'M': float(M), 'ColorOS': {'tag': ctag, 'intensity': cint}}
            tensor = encode_tensor_scalar(w, G, M, tokens)
            saved=self.mem.store(sym,it,tensor,metadata={'data':raw}, table=table)
            self.h5.append(sym,it,tensor)
            self.journal.log('mem_store', {'symbol':sym,'intent':it,'weight':w})
            return {'status':'MEM','saved':saved}
        elif branch=='out':
            self.tmp_memory.append(entry)
            self.journal.log('tmp_hold', {'weight':w})
            return {'status':'OUT','weight':w}
        else:
            self.tmp_memory.append(entry)
            return {'status':'TMP','weight':w}
    def daily(self):
        rep=daily_report(self.tmp_memory)
        import json
        from pathlib import Path
        Path('data/tmp_reports').mkdir(parents=True, exist_ok=True)
        p=Path('data/tmp_reports')/f"tmp_report_{rep['date']}.json"
        p.write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf-8')
        migrated=0
        # migrate high weight
        for e in list(self.tmp_memory):
            if e.get('weight',0)>=1.2:
                sym=e['features']['M']['symbol']; it=e['features']['M']['intent']
                # compute tensor and ColorOS
                tokens=e['features'].get('C',{}).get('tokens',0)
                G=e.get('G',0.0); M=e.get('M',0.0)
                from utils.color_os import color_tag
                ct = color_tag(M); ctag, cint = ct['tag'], ct['intensity']
                table={'Lp': len(self.mem.clusters.get(sym, type('x',(),{'entries':[]})).entries)+1 if hasattr(self.mem,'clusters') else 1,
                       'Ref': str(uuid.uuid4()), 'Date': __import__('datetime').datetime.utcnow().isoformat(),
                       'Context': e['features'].get('T',{}).get('type',''), 'Links': [], 'G': float(G), 'M': float(M), 'ColorOS': {'tag': ctag, 'intensity': cint}}
                from utils.tensors import encode_tensor_scalar
                tensor = encode_tensor_scalar(e['weight'], G, M, tokens)
                self.mem.store(sym,it,tensor,metadata={'data':e['data']}, table=table)
                self.h5.append(sym,it,tensor)
                self.tmp_memory.remove(e)
                migrated+=1
        # verification queue
        from pathlib import Path
        import json as _json
        vdir=Path('data/verify_queue'); vdir.mkdir(parents=True, exist_ok=True)
        vfile=vdir / f"verify_{rep['date']}.json"
        vfile.write_text(_json.dumps({'report':rep,'pending':migrated}, ensure_ascii=False, indent=2), encoding='utf-8')
        # after daily review, move TMP reports to archive (policy)
        from persistent.archive import rotate_tmp_reports
        rotate_tmp_reports()

        self.journal.log('daily_close', {'migrated':migrated,'report':rep})
        return {'report':rep,'migrated':migrated}
