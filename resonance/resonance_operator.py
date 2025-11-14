"""Operator applying resonance weights to tensors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .multiresonance_tensor import MultiresonanceTensor


@dataclass(slots=True)
class ResonanceOperator:
    tensor: MultiresonanceTensor

    def apply(self, vector: np.ndarray) -> np.ndarray:
        return self.tensor.normalised() @ vector


__all__ = ["ResonanceOperator"]
