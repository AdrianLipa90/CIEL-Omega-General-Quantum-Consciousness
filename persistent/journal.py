"""Append-only event journal for orchestrator operations."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class Journal:
    """Small audit helper that persists JSON lines."""

    def __init__(self, path: Path | str = Path("data/journal/log.jsonl")) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def log(self, event: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        payload = payload or {}
        entry = {"ts": datetime.utcnow().isoformat(), "event": event, "payload": payload}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry


__all__ = ["Journal"]
