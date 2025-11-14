"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Decision layer combining perception and prediction signals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .prediction import PredictiveCore


@dataclass(slots=True)
class DecisionCore:
    predictor: PredictiveCore = PredictiveCore()

    def decide(self, perception: Iterable[float], goals: Iterable[float]) -> float:
        score = self.predictor.forecast(perception)
        goal_alignment = np.mean(list(goals)) if list(goals) else 0.0
        return float(score + goal_alignment)


__all__ = ["DecisionCore"]
