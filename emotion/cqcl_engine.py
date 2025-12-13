"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

CIEL Quantum Consciousness Layer (CQCL) compatibility wrapper.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from fields.soul_invariant import SoulInvariant


@dataclass(slots=True)
class CIELQuantumEngine:
    invariant: SoulInvariant = field(default_factory=SoulInvariant)

    def evolve(self, psi: np.ndarray, steps: int = 1) -> np.ndarray:
        out = psi.astype(complex)
        for _ in range(max(steps, 0)):
            out *= np.exp(1j * 0.01)
            out = self.invariant.normalise(out)
        return out

    def coherence(self, psi: np.ndarray) -> float:
        return float(np.tanh(self.invariant.compute(psi)))


# Backwards compatible alias used by the historical extension modules.
CIEL_Quantum_Engine = CIELQuantumEngine

__all__ = ["CIELQuantumEngine", "CIEL_Quantum_Engine"]
