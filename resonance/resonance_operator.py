"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Operator applying resonance weights to tensors.
"""

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
