"""Translate EEG like traces into the emotional feature space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class EEGEmotionMapper:
    bands: List[str] = None

    def __post_init__(self) -> None:
        if self.bands is None:
            self.bands = ["delta", "theta", "alpha", "beta", "gamma"]

    def map(self, signal: Iterable[float]) -> dict[str, float]:
        values = list(signal)
        total = sum(values) or 1.0
        fractions = {band: values[i % len(values)] / total for i, band in enumerate(self.bands)}
        return fractions


__all__ = ["EEGEmotionMapper"]
