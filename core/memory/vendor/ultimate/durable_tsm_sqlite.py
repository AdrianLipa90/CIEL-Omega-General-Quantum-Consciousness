import json, sqlite3, hashlib
from pathlib import Path
from typing import Any, Dict
from .types import MemoriseD

class TSMWriterSQL:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self):
        return sqlite3.connect(str(self.db_path))

    def _init_schema(self):
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS memories (
    memorise_id TEXT PRIMARY KEY,
    created_at  TEXT NOT NULL,
    D_id        TEXT NOT NULL,
    D_context   TEXT,
    D_sense     TEXT,
    D_associations TEXT,
    D_timestamp TEXT,
    D_meta      TEXT,
    D_type      TEXT,
    D_attr      TEXT,
    W_L REAL, W_S REAL, W_K REAL, W_E REAL, W_F INTEGER,
    rationale   TEXT,
    source      TEXT,
    tsm_ref     TEXT,
    wpm_ref     TEXT,
    checksum    TEXT
)"""); conn.commit()

    def _checksum(self, record: MemoriseD) -> str:
        payload = (record.memorise_id + record.created_at + record.D_id + record.D_context + str(record.D_sense))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def save(self, record: MemoriseD) -> str:
        W = record.weights or {}
        checksum = self._checksum(record)
        with self._connect() as conn:
            conn.execute("""INSERT OR REPLACE INTO memories (
  memorise_id, created_at, D_id, D_context, D_sense, D_associations, D_timestamp, D_meta, D_type, D_attr,
  W_L, W_S, W_K, W_E, W_F, rationale, source, tsm_ref, wpm_ref, checksum
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",            (record.memorise_id, record.created_at, record.D_id, record.D_context, str(record.D_sense),
             json.dumps(record.D_associations, ensure_ascii=False), record.D_timestamp,
             json.dumps(record.D_meta, ensure_ascii=False), record.D_type, json.dumps(record.D_attr, ensure_ascii=False),
             float(W.get("W_L", 0.0)), float(W.get("W_S", 0.0)), float(W.get("W_K", 0.0)), float(W.get("W_E", 0.0)),
             1 if W.get("W_F", True) else 0, record.rationale, record.source, f"TSM:{record.memorise_id}", None, checksum))
            conn.commit()
        return f"TSM:{record.memorise_id}"

    def attach_wpm_ref(self, memorise_id: str, wpm_ref: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE memories SET wpm_ref = ? WHERE memorise_id = ?", (wpm_ref, memorise_id)); conn.commit()
