"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Translate EEG like traces into the emotional feature space.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .utils import fractional_distribution, to_signal_list


@dataclass(slots=True)
class EEGEmotionMapper:
    bands: List[str] = None

    def __post_init__(self) -> None:
        if self.bands is None:
            self.bands = ["delta", "theta", "alpha", "beta", "gamma"]

    def map(self, signal: Iterable[float]) -> dict[str, float]:
        values = to_signal_list(signal)
        return fractional_distribution(values, self.bands)


__all__ = ["EEGEmotionMapper"]
