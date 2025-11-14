"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Provide a Schumann resonance inspired clock.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import math
import time

import numpy as np


@dataclass(slots=True)
class SchumannClock:
    base_hz: float = 7.83
    start_t: float = field(default_factory=time.perf_counter)

    def phase(self, k: int = 1, at: Optional[float] = None) -> float:
        now = (time.perf_counter() - self.start_t) if at is None else at
        return (2.0 * math.pi * self.base_hz * k * now) % (2.0 * math.pi)

    def carrier(self, shape: Tuple[int, int], amp: float = 1.0, k: int = 1) -> np.ndarray:
        ph = self.phase(k=k)
        return amp * np.exp(1j * ph) * np.ones(shape, dtype=np.complex128)


__all__ = ["SchumannClock"]
