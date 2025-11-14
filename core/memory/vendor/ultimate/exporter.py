"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from pathlib import Path
from typing import Optional
import sqlite3, json, os

def export_raw_copy(db_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "memory_ledger.db"
    dst.write_bytes(Path(db_path).read_bytes())
    return dst

def export_jsonl(db_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "memories.jsonl"
    with sqlite3.connect(str(db_path)) as conn, dst.open("w", encoding="utf-8") as f:
        cur = conn.execute("SELECT * FROM memories")
        cols = [d[0] for d in cur.description]
        for row in cur.fetchall():
            rec = {c: row[i] for i, c in enumerate(cols)}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return dst

def export_parquet_or_csv(db_path: Path, out_dir: Path) -> Path:
    import pandas as pd
    out_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(db_path)) as conn:
        df = pd.read_sql_query("SELECT * FROM memories", conn)
    try:
        p = out_dir / "memories.parquet"
        df.to_parquet(p, index=False)
        return p
    except Exception:
        p = out_dir / "memories.csv"
        df.to_csv(p, index=False)
        return p
