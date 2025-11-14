"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Track mission milestones.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class MissionTracker:
    milestones: List[str] = field(default_factory=list)

    def add(self, milestone: str) -> None:
        self.milestones.append(milestone)


__all__ = ["MissionTracker"]
