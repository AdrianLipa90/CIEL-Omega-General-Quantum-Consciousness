"""Decision layer combining perception and prediction signals."""

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
