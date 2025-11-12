from pathlib import Path
from ciel_memory.orchestrator import UnifiedMemoryOrchestrator
from ciel_memory.exporter import export_raw_copy, export_jsonl, export_parquet_or_csv

def test_exporters(tmp_path: Path):
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context="Exp", sense="Export test long enough", meta={"novelty_hint": True})
    out = orch.run_tmp(D); refs = orch.user_force_save(D, out, reason="export-test")
    db = Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db")
    raw = export_raw_copy(db, tmp_path / "raw"); assert raw.exists()
    j = export_jsonl(db, tmp_path / "jsonl"); assert j.exists()
    tp = export_parquet_or_csv(db, tmp_path / "tbl"); assert tp.exists()
