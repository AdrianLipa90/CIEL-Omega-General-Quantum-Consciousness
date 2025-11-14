"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Safe numerical operations used across modules.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable

import numpy as np


def safe_inv(values: Iterable[float], eps: float = 1e-9) -> np.ndarray:
    arr = np.fromiter(values, dtype=float)
    arr = np.where(np.abs(arr) < eps, eps, arr)
    return 1.0 / arr


def heisenberg_soft_clip(x: np.ndarray | float, scale: float, eps: float = 1e-12) -> np.ndarray:
    """Smoothly saturate values without introducing hard cut-offs.

    Parameters
    ----------
    x:
        Value or array to be saturated.
    scale:
        Positive magnitude describing the asymptotic limit.  Values much
        smaller than ``scale`` remain effectively unchanged whereas larger
        magnitudes are smoothly compressed towards ``±scale``.
    eps:
        Tiny constant preventing division by zero when ``scale`` is extremely
        small.
    """

    s = float(scale) if scale is not None else 1.0
    if s <= 0.0:
        s = 1.0
    return s * np.tanh(np.asarray(x, dtype=float) / (s + eps))


def heisenberg_soft_clip_range(
    x: np.ndarray | float,
    lower: float,
    upper: float,
    eps: float = 1e-12,
) -> np.ndarray:
    """Heisenberg-inspired clip that honours an arbitrary numeric range."""

    if upper <= lower:
        raise ValueError("upper bound must be greater than lower bound")
    midpoint = 0.5 * (upper + lower)
    radius = 0.5 * (upper - lower)
    return midpoint + heisenberg_soft_clip(np.asarray(x, dtype=float) - midpoint, radius, eps)


__all__ = [
    "safe_inv",
    "heisenberg_soft_clip",
    "heisenberg_soft_clip_range",
]


class HeisenbergSoftClipper:
    """Stateful helper mirroring the non-linear saturation operator."""

    __slots__ = ("k_sigma", "history_limit", "_scales")

    def __init__(self, *, k_sigma: float = 2.0, history_limit: int = 128) -> None:
        self.k_sigma = float(k_sigma)
        self.history_limit = int(history_limit)
        self._scales: deque[float] = deque(maxlen=self.history_limit)

    def __call__(self, x: np.ndarray | float, scale: float | None = None) -> np.ndarray:
        arr = np.asarray(x, dtype=float)
        if scale is None:
            sigma = float(np.std(arr))
            if sigma == 0.0:
                sigma = float(np.max(np.abs(arr)) or 1.0)
            scale = max(self.k_sigma * sigma, 1e-12)
        result = heisenberg_soft_clip(arr, scale=float(scale))
        self._scales.append(float(scale))
        return result

    @property
    def last_scale(self) -> float:
        """Return the most recent uncertainty radius used by the clipper."""

        if not self._scales:
            return 0.0
        return float(self._scales[-1])

    @property
    def average_scale(self) -> float:
        """Return the rolling mean of the captured scales."""

        if not self._scales:
            return 0.0
        return float(np.mean(self._scales))


__all__.append("HeisenbergSoftClipper")
