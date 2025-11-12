#!/usr/bin/env python3
from pathlib import Path
import shutil
out = Path("export"); out.mkdir(exist_ok=True)
db = Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db")
if db.exists(): shutil.copy(db, out / "memory_ledger.db")
(out / "README.txt").write_text("Export bundle for CIEL-Memory Pro.")
print("Export ready:", out.resolve())
