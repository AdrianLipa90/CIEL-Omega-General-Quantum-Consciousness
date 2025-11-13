"""Aether field helpers built around :class:`~fields.intention_field.IntentionField`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from .intention_field import IntentionField


@dataclass(slots=True)
class AetherField:
    """Combine intention vectors into a smooth field representation."""

    intention: IntentionField
    smoothing: float = 0.2

    def realise(self, samples: Iterable[Iterable[float]]) -> np.ndarray:
        base = self.intention.generate()
        data: Sequence[Iterable[float]] = tuple(samples)
        accum = np.zeros_like(base)
        for row in data:
            arr = np.fromiter(row, dtype=float, count=base.size)
            if arr.size < base.size:
                arr = np.pad(arr, (0, base.size - arr.size))
            accum += arr
        if len(data):
            accum /= float(len(data))
        return (1 - self.smoothing) * base + self.smoothing * accum


__all__ = ["AetherField", "IntentionField"]
