"""Toy paradox filters used in symbolic routines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class ParadoxFilters:
    threshold: float = 0.5

    def filter(self, values: Iterable[float]) -> list[float]:
        return [v for v in values if abs(v) > self.threshold]


__all__ = ["ParadoxFilters"]
