"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Empathy engine computing similarity between emotional vectors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class EmpathicEngine:
    temperature: float = 1.0

    def compare(self, a: Iterable[float], b: Iterable[float]) -> float:
        av = np.fromiter(a, dtype=float)
        bv = np.fromiter(b, dtype=float)
        if av.size != bv.size:
            size = max(av.size, bv.size)
            av = np.pad(av, (0, size - av.size))
            bv = np.pad(bv, (0, size - bv.size))
        distance = np.linalg.norm(av - bv)
        return float(np.exp(-distance / max(self.temperature, 1e-6)))


__all__ = ["EmpathicEngine"]
