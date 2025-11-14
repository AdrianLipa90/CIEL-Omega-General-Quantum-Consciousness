"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Collection of ten deterministic experiments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any

import numpy as np

from evolution.omega_drift import OmegaDriftCore
from evolution.schumann_clock import SchumannClock


@dataclass(slots=True)
class CoreExperiments:
    drift: OmegaDriftCore = field(default_factory=lambda: OmegaDriftCore(SchumannClock()))

    def exp_constant_norm(self) -> Dict[str, Any]:
        psi = np.ones((16, 16), dtype=complex)
        out = self.drift.step(psi, sigma_scalar=1.0)
        return {"norm": float(np.linalg.norm(out))}

    def exp_phase_sweep(self) -> Dict[str, Any]:
        psi = np.ones((16, 16), dtype=complex)
        out = self.drift.step(psi, sigma_scalar=0.5)
        return {"phase_mean": float(np.angle(out).mean())}


__all__ = ["CoreExperiments"]
