"""Compact emotional core used by the high level tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable

from .utils import mean_and_variance, to_signal_list


@dataclass(slots=True)
class EmotionCore:
    baseline: float = 0.0
    history: list[Dict[str, float]] = field(default_factory=list, init=False, repr=False)

    def process(self, signal: Iterable[float]) -> Dict[str, float]:
        values = to_signal_list(signal)
        mood, variance = mean_and_variance(values, baseline=self.baseline)
        result = {"mood": mood, "variance": variance}
        self.history.append(result)
        return result


__all__ = ["EmotionCore"]
