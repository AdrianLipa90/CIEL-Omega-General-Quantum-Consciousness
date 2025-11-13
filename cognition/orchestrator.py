"""Glue logic combining cognition submodules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .decision import DecisionCore
from .intuition import IntuitiveCortex
from .perception import PerceptiveLayer
from .prediction import PredictiveCore


@dataclass(slots=True)
class CognitionOrchestrator:
    perception: PerceptiveLayer = field(default_factory=PerceptiveLayer)
    intuition: IntuitiveCortex = field(default_factory=IntuitiveCortex)
    prediction: PredictiveCore = field(default_factory=PredictiveCore)
    decision: DecisionCore = field(default_factory=DecisionCore)

    def evaluate(self, stimulus: Iterable[float], goals: Iterable[float]) -> dict[str, float]:
        perception_value = self.perception.perceive(stimulus)
        intuition_value = self.intuition.infer(stimulus)
        prediction_value = self.prediction.forecast(stimulus)
        decision_value = self.decision.decide(stimulus, goals)
        return {
            "perception": perception_value,
            "intuition": intuition_value,
            "prediction": prediction_value,
            "decision": decision_value,
        }


__all__ = ["CognitionOrchestrator"]
