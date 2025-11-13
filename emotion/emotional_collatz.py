"""Whimsical Collatz like iterator driving emotional sequences."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class EmotionalCollatzEngine:
    seed: int = 7

    def iterate(self, steps: int = 10) -> List[int]:
        value = self.seed
        sequence = [value]
        for _ in range(max(steps, 0)):
            if value % 2 == 0:
                value //= 2
            else:
                value = 3 * value + 1
            sequence.append(value)
        return sequence

    def mood_curve(self, scale: float = 0.1) -> List[float]:
        return [scale * v for v in self.iterate()]


__all__ = ["EmotionalCollatzEngine"]
