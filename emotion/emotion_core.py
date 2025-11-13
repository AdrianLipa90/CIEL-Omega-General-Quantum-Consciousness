"""Compact emotional core used by the high level tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


@dataclass(slots=True)
class EmotionCore:
    baseline: float = 0.0
    history: list[Dict[str, float]] = field(default_factory=list, init=False, repr=False)

    def process(self, signal: Iterable[float]) -> Dict[str, float]:
        values = list(signal)
        if not values:
            return {"mood": self.baseline, "variance": 0.0}
        mood = self.baseline + sum(values) / len(values)
        variance = sum((x - mood) ** 2 for x in values) / len(values)
        result = {"mood": mood, "variance": variance}
        self.history.append(result)
        return result


__all__ = ["EmotionCore"]
