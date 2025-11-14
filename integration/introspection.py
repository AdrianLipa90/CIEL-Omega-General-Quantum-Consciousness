"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Analyse dissociation between two signals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np


@dataclass(slots=True)
class DissociationAnalyzer:
    threshold: float = 0.3
    history: list[Dict[str, Any]] = field(default_factory=list, init=False)

    def step(self, ego: np.ndarray, world: np.ndarray) -> Dict[str, Any]:
        ego = (ego - ego.mean()) / (ego.std() + 1e-12)
        world = (world - world.mean()) / (world.std() + 1e-12)
        rho = float(np.dot(ego.ravel(), world.ravel()) / ego.size)
        state = "integration" if rho > self.threshold else "dissociation"
        payload = {"rho": rho, "state": state}
        self.history.append(payload)
        return payload


__all__ = ["DissociationAnalyzer"]
