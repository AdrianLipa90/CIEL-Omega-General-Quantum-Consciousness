"""Optimise resonance operators by gradient descent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .multiresonance_tensor import MultiresonanceTensor


@dataclass(slots=True)
class ResonanceOptimizer:
    tensor: MultiresonanceTensor
    lr: float = 0.1

    def step(self, target: Iterable[float]) -> None:
        vec = np.fromiter(target, dtype=float, count=self.tensor.channels)
        if vec.size < self.tensor.channels:
            vec = np.pad(vec, (0, self.tensor.channels - vec.size))
        grad = self.tensor.tensor @ vec
        self.tensor.tensor += self.lr * np.outer(vec, grad)


__all__ = ["ResonanceOptimizer"]
