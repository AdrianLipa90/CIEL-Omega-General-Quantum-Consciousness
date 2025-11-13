"""Synchronise memory entries across nodes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass(slots=True)
class MemorySync:
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def push(self, entry: Dict[str, Any]) -> None:
        self.entries.append(entry)

    def pull(self) -> List[Dict[str, Any]]:
        return list(self.entries)


__all__ = ["MemorySync"]
