from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def laplacian2(a: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a, dtype=a.dtype)
    out[1:-1, 1:-1] = a[2:, 1:-1] + a[:-2, 1:-1] + a[1:-1, 2:] + a[1:-1, :-2] - 4.0 * a[1:-1, 1:-1]
    return out