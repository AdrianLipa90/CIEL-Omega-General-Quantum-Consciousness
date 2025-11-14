"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Utilities for rotating temporary TMP reports.
"""
from __future__ import annotations

import shutil
from pathlib import Path


def rotate_tmp_reports(source: Path | str = Path("data/tmp_reports"), destination: Path | str = Path("data/archive")) -> dict:
    """Move tmp report files into an archive folder."""

    source_path = Path(source)
    destination_path = Path(destination)
    destination_path.mkdir(parents=True, exist_ok=True)
    moved = 0
    if source_path.exists():
        for file in source_path.glob("*.json"):
            target = destination_path / file.name
            shutil.move(str(file), target)
            moved += 1
    return {"moved": moved, "destination": str(destination_path)}


__all__ = ["rotate_tmp_reports"]
