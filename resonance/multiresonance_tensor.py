"""Tensor container aggregating resonance amplitudes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class MultiresonanceTensor:
    channels: int = 12
    tensor: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.tensor = np.zeros((self.channels, self.channels), dtype=float)

    def accumulate(self, samples: Iterable[float]) -> None:
        vec = np.fromiter(samples, dtype=float, count=self.channels)
        if vec.size < self.channels:
            vec = np.pad(vec, (0, self.channels - vec.size))
        outer = np.outer(vec, vec)
        self.tensor += outer

    def normalised(self) -> np.ndarray:
        norm = np.linalg.norm(self.tensor) or 1.0
        return self.tensor / norm


__all__ = ["MultiresonanceTensor"]
