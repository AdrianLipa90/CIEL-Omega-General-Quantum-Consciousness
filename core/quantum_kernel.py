"""CIEL/Ω Quantum Consciousness Suite
 
 Copyright (c) 2025 Adrian Lipa / Intention Lab
 Licensed under the CIEL Research Non-Commercial License v1.1.
 """

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from mathematics.safe_operations import resonance


@dataclass(slots=True)
class CIELPhysics:
    c: float = 299_792_458.0
    hbar: float = 1.054_571_817e-34
    G: float = 6.67430e-11

    LIPA_CONSTANT: float = 0.474812
    MAX_COHERENCE: float = 0.751234
    ETHICAL_BOUND: float = 0.900000


def normalise_field(field: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    arr = np.asarray(field)
    n = float(np.linalg.norm(arr))
    if n < eps:
        return arr
    return arr / n


def resonance_measure(a: np.ndarray, b: np.ndarray) -> float:
    return resonance(a, b)


__all__ = [
    "CIELPhysics",
    "normalise_field",
    "resonance_measure",
]
