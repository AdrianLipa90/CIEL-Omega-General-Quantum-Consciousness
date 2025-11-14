"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Predictive layer implementing a minimal linear model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class PredictiveCore:
    horizon: int = 3

    def forecast(self, signal: Iterable[float]) -> float:
        values = np.fromiter(signal, dtype=float)
        if values.size == 0:
            return 0.0
        coeffs = np.linspace(1.0, 2.0, min(self.horizon, values.size))
        recent = values[-coeffs.size :]
        return float(np.dot(coeffs, recent) / coeffs.sum())


__all__ = ["PredictiveCore"]
