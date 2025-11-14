"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Adam-like optimiser applied to memory traces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class AdamMemoryKernel:
    beta1: float = 0.9
    beta2: float = 0.999
    epsilon: float = 1e-8
    m: np.ndarray | None = field(default=None, init=False)
    v: np.ndarray | None = field(default=None, init=False)
    step_count: int = field(default=0, init=False)

    def update(self, gradient: Iterable[float]) -> np.ndarray:
        g = np.fromiter(gradient, dtype=float)
        if self.m is None:
            self.m = np.zeros_like(g)
            self.v = np.zeros_like(g)
        self.step_count += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * g
        self.v = self.beta2 * self.v + (1 - self.beta2) * (g ** 2)
        m_hat = self.m / (1 - self.beta1 ** self.step_count)
        v_hat = self.v / (1 - self.beta2 ** self.step_count)
        return m_hat / (np.sqrt(v_hat) + self.epsilon)


__all__ = ["AdamMemoryKernel"]
