"""Ritual module combining mission tracker with intention fields."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from fields.intention_field import IntentionField


@dataclass(slots=True)
class RitualModule:
    intention: IntentionField = field(default_factory=IntentionField)

    def perform(self, steps: Iterable[str]) -> float:
        self.intention.reset()
        return sum(len(step) for step in steps) / 100.0


__all__ = ["RitualModule"]
