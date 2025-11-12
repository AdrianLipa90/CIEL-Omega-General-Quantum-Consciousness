import json
from pathlib import Path
from datetime import datetime

class Journal:
    def __init__(self, root='data/journal'):
        self.root=Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def log(self, event:str, payload:dict):
        rec={'ts':datetime.utcnow().isoformat(),'event':event,'payload':payload}
        day=datetime.utcnow().strftime('%Y%m%d')
        p=self.root / f'journal_{day}.jsonl'
        with p.open('a',encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False)+'\n')
        return str(p)
