"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Wave bit utilities for small three dimensional chunks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(slots=True)
class WaveBit3D:
    shape: Tuple[int, int, int] = (4, 4, 4)

    def make(self) -> np.ndarray:
        grid = np.indices(self.shape).sum(axis=0)
        return np.sin(grid)


@dataclass(slots=True)
class ConsciousWaveBit3D(WaveBit3D):
    def make(self) -> np.ndarray:
        base = super().make()
        return np.tanh(base)


__all__ = ["WaveBit3D", "ConsciousWaveBit3D"]
