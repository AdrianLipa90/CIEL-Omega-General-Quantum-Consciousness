"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Cognition specific helpers built on top of :mod:`fields.intention_field`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from fields.intention_field import IntentionField


@dataclass(slots=True)
class CognitiveIntentionField(IntentionField):
    """Specialised variant that exposes semantic projection helpers."""

    def coherence(self, signal: Iterable[float]) -> float:
        """Return a bounded coherence measure between ``signal`` and the field."""

        projection = self.project(signal)
        return float(np.tanh(abs(projection)))


__all__ = ["CognitiveIntentionField", "IntentionField"]
