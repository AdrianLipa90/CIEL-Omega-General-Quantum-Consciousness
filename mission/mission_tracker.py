"""Track mission milestones."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class MissionTracker:
    milestones: List[str] = field(default_factory=list)

    def add(self, milestone: str) -> None:
        self.milestones.append(milestone)


__all__ = ["MissionTracker"]
