"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Generate simple TMP review reports.
"""
from __future__ import annotations

from datetime import date
from typing import Iterable, Mapping


def daily_report(entries: Iterable[Mapping[str, object]]) -> dict:
    """Build a deterministic report from *entries*."""

    entries = list(entries)
    promoted = sum(1 for e in entries if e.get("status") == "MEM")
    held = sum(1 for e in entries if e.get("status") == "TMP")
    discarded = sum(1 for e in entries if e.get("status") == "OUT")
    return {
        "date": date.today().isoformat(),
        "counts": {"promoted": promoted, "held": held, "discarded": discarded},
        "total": len(entries),
    }


__all__ = ["daily_report"]
