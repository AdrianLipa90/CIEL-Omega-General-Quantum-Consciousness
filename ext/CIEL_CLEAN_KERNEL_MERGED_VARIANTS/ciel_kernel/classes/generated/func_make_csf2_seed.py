from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List
import numpy as np, json, math

def make_csf2_seed(n: int=96) -> CSF2State:
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.2 * Y))
    sigma = np.exp(-(X ** 2 + Y ** 2) / 2.0)
    lam = np.ones_like(psi) * 0.1
    omega = np.zeros_like(sigma)
    psi = psi / (np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12)
    return CSF2State(psi.astype(np.complex128), sigma.astype(np.float64), lam.astype(np.complex128), omega.astype(np.float64))