"""Light-weight representation of the unified reality laws."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass(slots=True)
class UnifiedRealityLaws:
    constants: Dict[str, float]

    def lagrangian_density(self, psi: np.ndarray) -> float:
        grad = np.gradient(psi)
        energy = sum(np.mean(np.abs(g) ** 2) for g in grad)
        potential = self.constants.get("potential", 1.0) * np.mean(np.abs(psi) ** 2)
        return float(energy + potential)


__all__ = ["UnifiedRealityLaws"]
