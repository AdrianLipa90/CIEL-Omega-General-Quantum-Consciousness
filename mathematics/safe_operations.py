"""Safe numerical operations used across modules."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def safe_inv(values: Iterable[float], eps: float = 1e-9) -> np.ndarray:
    arr = np.fromiter(values, dtype=float)
    arr = np.where(np.abs(arr) < eps, eps, arr)
    return 1.0 / arr


__all__ = ["safe_inv"]
