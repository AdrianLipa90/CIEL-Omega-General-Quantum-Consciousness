from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def exp_rcde_calibrated() -> Dict[str, Any]:
    """Homeostat Σ↔Ψ."""
    psi, _, _ = make_seed()
    rcde = RCDECalibrator(lam=0.25, dt=0.05, sigma=0.6)
    sigmas = []
    for _ in range(30):
        psi = psi + 1j * 0.01 * laplacian2(psi)
        psi /= field_norm(psi)
        sigmas.append(rcde.step(psi))
    return {'sigma_last': float(sigmas[-1]), 'sigma_mean': float(np.mean(sigmas))}