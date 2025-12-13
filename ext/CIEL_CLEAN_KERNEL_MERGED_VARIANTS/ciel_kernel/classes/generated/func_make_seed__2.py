from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

def make_seed(n: int=96) -> CSF2State:
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.2 * Y))
    psi /= _norm(psi) + 1e-12
    sigma = np.exp(-(X ** 2 + Y ** 2) / 2.0)
    lam = np.ones_like(psi) * 0.1
    omega = np.zeros_like(sigma)
    return CSF2State(psi.astype(np.complex128), sigma.astype(np.float64), lam.astype(np.complex128), omega.astype(np.float64))