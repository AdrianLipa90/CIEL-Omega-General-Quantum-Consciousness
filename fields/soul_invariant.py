"""Simplified soul invariant metric used by multiple subsystems."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class SoulInvariant:
    """Compute a log-weighted power measure of a complex field."""

    epsilon: float = 1e-12

    def compute(self, field: np.ndarray) -> float:
        fft = np.fft.fft2(field)
        power = np.abs(fft) ** 2
        h, w = field.shape
        ky = np.fft.fftfreq(h)
        kx = np.fft.fftfreq(w)
        spectrum = power * np.log1p(ky[:, None] ** 2 + kx[None, :] ** 2 + self.epsilon)
        return float(np.mean(spectrum))

    def normalise(self, field: np.ndarray) -> np.ndarray:
        value = self.compute(field)
        scale = np.sqrt(abs(value)) + self.epsilon
        return field / scale


__all__ = ["SoulInvariant"]
