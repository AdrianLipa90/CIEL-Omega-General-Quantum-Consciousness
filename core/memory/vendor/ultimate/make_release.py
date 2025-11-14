#!/usr/bin/env python3
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import hashlib, zipfile, os, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
target = root / "CIEL-Memory-Ultimate-Release.zip"
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for folder in ["src", "configs", "docs", "CONTRACTS", "scripts", "examples", "tests"]:
        for r, _, files in os.walk(root / folder):
            for f in files:
                fp = pathlib.Path(r) / f
                z.write(fp, fp.relative_to(root).as_posix())
    for f in ["pyproject.toml", "README.md", "LICENSE", "Makefile"]:
        z.write(root / f, f)
sha = hashlib.sha256(target.read_bytes()).hexdigest()
(root / "SHA256.txt").write_text(f"{sha}  {target.name}\n")
print("Release:", target)
print("SHA256:", sha)
