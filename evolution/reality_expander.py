"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Procedural reality expander producing synthetic frames.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class RealityExpander:
    grid: int = 64

    def expand(self, seeds: Iterable[float]) -> np.ndarray:
        arr = np.fromiter(seeds, dtype=float, count=self.grid * self.grid)
        if arr.size < self.grid * self.grid:
            arr = np.pad(arr, (0, self.grid * self.grid - arr.size))
        return arr.reshape(self.grid, self.grid)


__all__ = ["RealityExpander"]
