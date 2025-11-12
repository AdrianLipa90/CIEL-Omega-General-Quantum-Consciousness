from pathlib import Path
from typing import Dict, Any
import json, datetime as dt

class AuditLog:
    def __init__(self, path: Path = Path("CIEL_MEMORY_SYSTEM/AUDIT/ledger.jsonl")):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def append(self, event: str, payload: Dict[str, Any]) -> None:
        rec = {"ts": dt.datetime.utcnow().isoformat(), "event": event, "payload": payload}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
