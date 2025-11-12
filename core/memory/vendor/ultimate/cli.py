import argparse, json, sys, zipfile, hashlib, os
from pathlib import Path
from .orchestrator import UnifiedMemoryOrchestrator
from .exporter import export_raw_copy, export_jsonl, export_parquet_or_csv

def cmd_status(args):
    print("[CIEL-Memory Ultimate] status OK")
    print("DB:", Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db").resolve())
    print("H5:", Path("CIEL_MEMORY_SYSTEM/WPM/wave_snapshots/wave_archive.h5").resolve())
    print("AUDIT:", Path("CIEL_MEMORY_SYSTEM/AUDIT/ledger.jsonl").resolve())

def cmd_run(args):
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context=args.context, sense=args.sense, meta={"novelty_hint": args.novelty})
    out = orch.run_tmp(D)
    print("TMP OUT:", json.dumps(out["OUT"], indent=2, ensure_ascii=False))
    if args.promote:
        refs = orch.promote_if_bifurcated(D, out)
        if not refs and args.override:
            refs = orch.user_force_save(D, out, reason="cli-override")
        print("Durable:", refs)

def cmd_promote(args):
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context=args.context, sense=args.sense, meta={"trusted_source": True})
    out = orch.run_tmp(D)
    refs = orch.promote_if_bifurcated(D, out)
    print("Promote result:", refs)

def cmd_override(args):
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context=args.context, sense=args.sense, meta={"trusted_source": True})
    out = orch.run_tmp(D)
    refs = orch.user_force_save(D, out, reason=args.reason or "override")
    print("Override result:", refs)

def cmd_verify(args):
    orch = UnifiedMemoryOrchestrator()
    stats = orch.daily_maintenance()
    print("Verification queue stats:", stats)

def cmd_backup(args):
    target = Path(args.output or "ciel_memory_backup.zip")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for base in ["CIEL_MEMORY_SYSTEM", "configs", "CONTRACTS", "docs"]:
            for root, _, files in os.walk(base):
                for f in files:
                    p = Path(root) / f
                    z.write(p, p.as_posix())
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    print("Backup:", target, "SHA256:", sha)

def cmd_export(args):
    out = Path(args.output or "export_raw")
    copy = export_raw_copy(Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db"), out)
    print("Raw DB export:", copy.resolve())

def cmd_export2(args):
    out = Path(args.output or "export_data")
    db = Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db")
    j = export_jsonl(db, out)
    p = export_parquet_or_csv(db, out)
    print("JSONL:", j.resolve())
    print("Tabular:", p.resolve())

def cmd_wavesave(args):
    import numpy as np
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context="wave", sense="wave snapshot demo", meta={"trusted_source": True})
    out = orch.run_tmp(D)
    wave = {"amplitude": np.random.rand(64,64).astype("float32"), "phase": np.random.rand(64,64).astype("float32")}
    refs = orch.user_force_save(D, out, reason="wavesave", wave_arrays=wave, wave_attrs={"grid":"64x64"})
    print("Wave saved:", refs)

def cmd_dashboard(args):
    try:
        import streamlit as st  # noqa
    except Exception:
        print("Install extras: pip install -e '.[dashboard]'", file=sys.stderr)
        return 2
    os.execvp("streamlit", ["streamlit", "run", "src/ciel_memory/dashboard_app.py"])

def main(argv=None):
    p = argparse.ArgumentParser(prog="cielmem", description="CIEL-Memory Ultimate CLI")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("status", help="Show status and paths"); s.set_defaults(func=cmd_status)

    r = sub.add_parser("run", help="Run TMP and optionally promote/override")
    r.add_argument("--context", required=True); r.add_argument("--sense", required=True)
    r.add_argument("--novelty", action="store_true"); r.add_argument("--promote", action="store_true")
    r.add_argument("--override", action="store_true"); r.set_defaults(func=cmd_run)

    pr = sub.add_parser("promote", help="Force run and promote if B=1"); pr.add_argument("--context", required=True); pr.add_argument("--sense", required=True); pr.set_defaults(func=cmd_promote)

    ov = sub.add_parser("override", help="Force durable write"); ov.add_argument("--context", required=True); ov.add_argument("--sense", required=True); ov.add_argument("--reason"); ov.set_defaults(func=cmd_override)

    v = sub.add_parser("verify", help="Daily maintenance/verification"); v.set_defaults(func=cmd_verify)

    b = sub.add_parser("backup", help="Create ZIP backup + checksum"); b.add_argument("-o","--output"); b.set_defaults(func=cmd_backup)

    e = sub.add_parser("export", help="Export raw SQLite copy"); e.add_argument("-o","--output"); e.set_defaults(func=cmd_export)

    e2 = sub.add_parser("export2", help="Export JSONL + Parquet (or CSV fallback)"); e2.add_argument("-o","--output"); e2.set_defaults(func=cmd_export2)

    w = sub.add_parser("wavesave", help="Demo: save wave arrays"); w.set_defaults(func=cmd_wavesave)

    d = sub.add_parser("dashboard", help="Run Streamlit dashboard"); d.set_defaults(func=cmd_dashboard)

    args = p.parse_args(argv)
    if not getattr(args, "cmd", None): p.print_help(); return 1
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
