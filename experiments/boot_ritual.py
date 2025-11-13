"""Simplified boot ritual orchestrating the drift core."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np

from evolution.omega_drift import OmegaDriftCore
from evolution.schumann_clock import SchumannClock


@dataclass(slots=True)
class OmegaBootRitual:
    drift: OmegaDriftCore = field(default_factory=lambda: OmegaDriftCore(SchumannClock()))
    steps: int = 8

    def run(self, psi: np.ndarray) -> Dict[str, Any]:
        sigma = 1.0
        state = psi.astype(complex)
        for _ in range(self.steps):
            state = self.drift.step(state, sigma)
            sigma = float(np.clip(np.mean(np.abs(state) ** 2), 0.0, 1.2))
        return {"psi": state, "sigma": sigma}


__all__ = ["OmegaBootRitual"]
