import argparse, json, sys, zipfile, hashlib, os
from pathlib import Path
from .orchestrator import UnifiedMemoryOrchestrator

def cmd_status(args):
    print("[CIEL-Memory Pro] status OK")
    print("DB:", Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db").resolve())
    print("H5:", Path("CIEL_MEMORY_SYSTEM/WPM/wave_snapshots/wave_archive.h5").resolve())

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
    # simple export: SQLite copy + minimal JSONL meta (if exists)
    out = Path(args.output or "export")
    out.mkdir(parents=True, exist_ok=True)
    src_db = Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db")
    if src_db.exists():
        dst_db = out / "memory_ledger.db"
        dst_db.write_bytes(src_db.read_bytes())
    # JSONL index (if any)
    (out / "README.txt").write_text("Export bundle for CIEL-Memory Pro.")
    print("Export ready at:", out.resolve())

def cmd_wavesave(args):
    import numpy as np
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context="wave", sense="wave snapshot demo", meta={"trusted_source": True})
    out = orch.run_tmp(D)
    # Force save with fake wave arrays
    wave = {"amplitude": np.random.rand(64,64).astype("float32"), "phase": np.random.rand(64,64).astype("float32")}
    refs = orch.user_force_save(D, out, reason="wavesave", wave_arrays=wave, wave_attrs={"grid":"64x64"})
    print("Wave saved:", refs)

def main(argv=None):
    p = argparse.ArgumentParser(prog="cielmem", description="CIEL-Memory Pro CLI")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("status", help="Show status and paths"); s.set_defaults(func=cmd_status)
    r = sub.add_parser("run", help="Run TMP and optionally promote")
    r.add_argument("--context", required=True); r.add_argument("--sense", required=True)
    r.add_argument("--novelty", action="store_true"); r.add_argument("--promote", action="store_true")
    r.add_argument("--override", action="store_true"); r.set_defaults(func=cmd_run)
    v = sub.add_parser("verify", help="Daily maintenance/verification"); v.set_defaults(func=cmd_verify)
    b = sub.add_parser("backup", help="Create ZIP backup + checksum"); b.add_argument("-o","--output"); b.set_defaults(func=cmd_backup)
    e = sub.add_parser("export", help="Export durable memory bundle"); e.add_argument("-o","--output"); e.set_defaults(func=cmd_export)
    w = sub.add_parser("wavesave", help="Demo: save wave arrays"); w.set_defaults(func=cmd_wavesave)
    args = p.parse_args(argv)
    if not getattr(args, "cmd", None): p.print_help(); return 1
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
