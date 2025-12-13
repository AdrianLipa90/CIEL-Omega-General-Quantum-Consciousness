from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Any, List
import numpy as np
import scipy.linalg as la
import h5py
import warnings
import matplotlib.pyplot as plt
from scipy import sparse
import cmath
import math

def unified_lambda0(phys: CIELPhysics, B: np.ndarray, rho: np.ndarray, L_scale: float, F: np.ndarray, alpha_res: np.ndarray):
    rho_safe = np.maximum(rho, 1e-30)
    plasma = B ** 2 / (phys.mu0 * rho_safe * phys.c ** 2) * (1.0 / max(L_scale ** 2, 1e-60)) * alpha_res
    divF = sum((np.gradient(F[..., mu], axis=mu if mu < 3 else 3) for mu in range(4)))
    curlF2 = 0.0
    for a in range(4):
        for b in range(a + 1, 4):
            curlF2 += (np.gradient(F[..., b], axis=a) - np.gradient(F[..., a], axis=b)) ** 2
    topo = phys.beta * (divF ** 2 - curlF2)
    return plasma + topo