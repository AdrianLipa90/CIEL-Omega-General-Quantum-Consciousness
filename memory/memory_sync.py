"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Synchronise memory entries across nodes.
"""

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
