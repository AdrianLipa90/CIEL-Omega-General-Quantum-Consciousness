"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Pre-process EEG traces for the rest of the pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class EEGProcessor:
    sample_rate: float = 128.0

    def filter(self, signal: Iterable[float]) -> np.ndarray:
        values = np.fromiter(signal, dtype=float)
        if values.size == 0:
            return values
        freqs = np.fft.rfftfreq(values.size, d=1.0 / self.sample_rate)
        spectrum = np.fft.rfft(values)
        spectrum[freqs > 40.0] = 0.0
        return np.fft.irfft(spectrum, n=values.size)


__all__ = ["EEGProcessor"]
