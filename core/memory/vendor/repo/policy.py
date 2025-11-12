import json, pathlib

class Policy:
    def __init__(self, path='config/policies.json'):
        self.path=pathlib.Path(path)
        self.conf=json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {}
    def immutable_boost(self, data, features):
        boost=0.0
        for r in self.conf.get('immutable_rules',[]):
            if r['type']=='keyword' and isinstance(data,str) and r['value'].lower() in data.lower():
                boost=max(boost,float(r.get('weight',0)))
            if r['type']=='tag' and r['value'] in features.get('M',{}).get('tags',[]):
                boost=max(boost,float(r.get('weight',0)))
        return boost
    def float_boost_user(self, data, features):
        add=0.0
        for r in self.conf.get('float_rules_user',[]):
            if r['type']=='length_threshold' and isinstance(data,str) and len(data)>=int(r['gte']):
                add+=float(r.get('add',0))
            if r['type']=='contains' and isinstance(data,str):
                if any(k.lower() in data.lower() for k in r.get('value', [])):
                    add+=float(r.get('add',0))
        return add
    def float_boost_self(self, data, features):
        add=0.0
        for r in self.conf.get('float_rules_self',[]):
            if r['type']=='interest_symbol' and features.get('M',{}).get('symbol') in r.get('symbols',[]):
                add+=float(r.get('add',0))
            if r['type']=='intent_match' and features.get('M',{}).get('intent') in r.get('intents',[]):
                add+=float(r.get('add',0))
        return add
    def spectral_conf(self):
        return self.conf.get('spectral', {'base':1.0,'G_weight':0.6,'M_weight':0.4,'cap_low':-1.0,'cap_high':1.0,'decision':{'to_mem':1.65,'to_out':0.50}})
