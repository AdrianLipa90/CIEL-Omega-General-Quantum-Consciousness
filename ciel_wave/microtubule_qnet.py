"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Microtubule quantum network toy model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class MicrotubuleQNet:
    nodes: int = 8

    def propagate(self, signal: Iterable[float]) -> np.ndarray:
        vec = np.fromiter(signal, dtype=float, count=self.nodes)
        if vec.size < self.nodes:
            vec = np.pad(vec, (0, self.nodes - vec.size))
        matrix = np.eye(self.nodes) + 0.1 * np.ones((self.nodes, self.nodes))
        return matrix @ vec


__all__ = ["MicrotubuleQNet"]
