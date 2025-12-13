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

class SoulInvariantOperator:
    """Σ̂ = exp(i ∮_C A_φ ⋅ dℓ) – całka po pętli fazowej"""

    def __init__(self, Aphi: np.ndarray, loop_xyz: np.ndarray):
        self.Aphi = np.asarray(Aphi, dtype=np.complex128)
        self.loop = np.asarray(loop_xyz, dtype=float)

    def compute(self) -> complex:
        dL = np.diff(self.loop[:, :2], axis=0)
        dl_complex = dL[:, 0] + 1j * dL[:, 1]
        integrand = np.sum(self.Aphi[:len(dl_complex)] * dl_complex)
        return np.exp(1j * integrand)