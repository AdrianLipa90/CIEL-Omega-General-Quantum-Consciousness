from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

def _coh(psi: np.ndarray) -> float:
    gx = np.zeros_like(psi)
    gy = np.zeros_like(psi)
    gx[:, 1:-1] = psi[:, 2:] - psi[:, :-2]
    gy[1:-1, :] = psi[2:, :] - psi[:-2, :]
    E = np.mean(np.abs(gx) ** 2 + np.abs(gy) ** 2)
    return float(1.0 / (1.0 + E))