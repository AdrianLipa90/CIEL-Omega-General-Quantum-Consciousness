"""Safe numerical operations used across modules."""

from __future__ import annotations

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
