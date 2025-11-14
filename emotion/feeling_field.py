"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Field level aggregation of emotional signals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class FeelingField:
    decay: float = 0.95

    def integrate(self, signal: Iterable[float]) -> np.ndarray:
        values = np.fromiter(signal, dtype=float)
        window = np.exp(-np.arange(values.size) / max(self.decay, 1e-6))
        return values * window


__all__ = ["FeelingField"]
