"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Light-weight perception layer using moving averages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class PerceptiveLayer:
    window: int = 5

    def perceive(self, signal: Iterable[float]) -> float:
        values = np.fromiter(signal, dtype=float)
        if values.size == 0:
            return 0.0
        w = min(self.window, values.size)
        return float(values[-w:].mean())


__all__ = ["PerceptiveLayer"]
