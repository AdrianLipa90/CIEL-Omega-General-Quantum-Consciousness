"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

High level orchestrator gluing together the emotional submodules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .emotion_core import EmotionCore
from .empathy import EmpathicEngine
from .feeling_field import FeelingField


@dataclass(slots=True)
class AffectiveOrchestrator:
    core: EmotionCore = field(default_factory=EmotionCore)
    empathy: EmpathicEngine = field(default_factory=EmpathicEngine)
    field: FeelingField = field(default_factory=FeelingField)

    def run(self, ego: Iterable[float], other: Iterable[float]) -> dict[str, float]:
        core_metrics = self.core.process(ego)
        empathy_score = self.empathy.compare(ego, other)
        field_vec = self.field.integrate(ego)
        return {
            "mood": core_metrics["mood"],
            "empathy": empathy_score,
            "field_power": float(field_vec.mean() if field_vec.size else 0.0),
        }


__all__ = ["AffectiveOrchestrator"]
