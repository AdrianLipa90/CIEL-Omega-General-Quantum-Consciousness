"""Simple long term memory storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any

import json


@dataclass(slots=True)
class LongTermMemory:
    path: Path
    entries: list[Dict[str, Any]] = field(default_factory=list, init=False)

    def store(self, entry: Dict[str, Any]) -> None:
        self.entries.append(entry)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.entries, ensure_ascii=False, indent=2), encoding="utf-8")


__all__ = ["LongTermMemory"]
