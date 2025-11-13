"""Lambda₀ operator translating invariants into ethical guidance."""

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
