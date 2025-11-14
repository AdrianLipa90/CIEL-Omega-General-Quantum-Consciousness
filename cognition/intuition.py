"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Simplified intuition layer used in tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class IntuitiveCortex:
    def infer(self, signal: Iterable[float]) -> float:
        arr = np.fromiter(signal, dtype=float)
        return float(np.median(arr) if arr.size else 0.0)


__all__ = ["IntuitiveCortex"]
