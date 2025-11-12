import numpy as np
from datetime import datetime

class Cluster:
    def __init__(self, symbol:str):
        self.symbol=symbol; self.entries=[]
    def add_entry(self, intent, vector, metadata=None, table=None):
        e={'symbol':self.symbol,'intent':intent,'vector':[float(x) for x in vector],'timestamp':datetime.utcnow().isoformat(),'metadata':metadata or {}, 'table': table or {}}
        self.entries.append(e); return e
    def find_similar(self, vector, threshold=0.5):
        vec=np.array(vector,dtype=float); sims=[]
        for e in self.entries:
            v=np.array(e['vector'],dtype=float)
            denom=np.linalg.norm(v)*np.linalg.norm(vec)
            if denom==0: continue
            cos=float(np.dot(v,vec)/denom)
            if cos>threshold: sims.append(e)
        return sims

class PersistentMemory:
    def __init__(self): self.clusters={}
    def store(self, symbol, intent, vector, mode='auto', metadata=None):
        if symbol not in self.clusters: self.clusters[symbol]=Cluster(symbol)
        return self.clusters[symbol].add_entry(intent, vector, metadata)
    def query(self, symbol=None, intent=None):
        res=[]
        for sym,cl in self.clusters.items():
            if symbol and sym!=symbol: continue
            for e in cl.entries:
                if intent and e['intent']!=intent: continue
                res.append(e)
        return res
    def collapse_cluster(self, symbol):
        if symbol not in self.clusters: return False
        cl=self.clusters[symbol]
        if not cl.entries: return False
        mat=[np.array(e['vector'],dtype=float) for e in cl.entries if e['vector']]
        if not mat: return False
        import numpy as np
        med=np.median(np.vstack(mat),axis=0).tolist()
        for e in cl.entries: e['vector']=med
        return True
