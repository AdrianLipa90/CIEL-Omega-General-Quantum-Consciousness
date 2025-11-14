"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Biological forcing field based on the intention vector.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from fields.intention_field import IntentionField


@dataclass(slots=True)
class ForcingField:
    intention: IntentionField

    def stimulate(self, signal: Iterable[float]) -> np.ndarray:
        projection = self.intention.project(signal)
        return self.intention.generate() * projection


__all__ = ["ForcingField", "IntentionField"]
