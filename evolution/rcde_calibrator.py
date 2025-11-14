"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Homeostat maintaining a target sigma based on field energy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from mathematics.safe_operations import heisenberg_soft_clip_range


def _energy(field: np.ndarray) -> float:
    return float(np.mean(np.abs(field) ** 2))


@dataclass(slots=True)
class RCDECalibrator:
    lam: float = 0.2
    dt: float = 0.05
    sigma: float = 0.5

    def step(self, psi: np.ndarray) -> float:
        target = _energy(psi)
        self.sigma = float(self.sigma + self.dt * self.lam * (target - self.sigma))
        self.sigma = float(heisenberg_soft_clip_range(self.sigma, 0.0, 1.5))
        return self.sigma


__all__ = ["RCDECalibrator"]
