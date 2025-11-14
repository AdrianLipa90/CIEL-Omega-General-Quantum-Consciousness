"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Lambda₀ operator translating invariants into ethical guidance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from fields.soul_invariant import SoulInvariant


@dataclass(slots=True)
class Lambda0Operator:
    invariant: SoulInvariant

    def evaluate(self, field: np.ndarray) -> float:
        sigma = self.invariant.compute(field)
        return float(np.tanh(sigma))


__all__ = ["Lambda0Operator"]
