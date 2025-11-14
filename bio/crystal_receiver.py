"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Receiver translating crystal vibrations into the intention space.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from fields.intention_field import IntentionField


@dataclass(slots=True)
class CrystalFieldReceiver:
    intention: IntentionField

    def receive(self, vibration: Iterable[float]) -> np.ndarray:
        vec = np.fromiter(vibration, dtype=float)
        if vec.size == 0:
            return self.intention.generate()
        return self.intention.generate() + vec / (np.linalg.norm(vec) or 1.0)


__all__ = ["CrystalFieldReceiver"]
