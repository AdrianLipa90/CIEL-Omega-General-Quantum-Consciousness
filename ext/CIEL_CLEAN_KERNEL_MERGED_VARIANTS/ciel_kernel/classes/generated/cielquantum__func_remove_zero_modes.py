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

def remove_zero_modes(H, tol=1e-10, fudge=1e-08):
    """Hermitian projector on near-null subspace + pseudoinverse"""
    vals, vecs = la.eigh(H)
    small = np.abs(vals) < tol
    P0 = vecs[:, small] @ vecs[:, small].conj().T if small.any() else np.zeros_like(H)
    inv_vals = np.zeros_like(vals)
    inv_vals[~small] = 1.0 / vals[~small]
    inv_vals[small] = 1.0 / fudge
    H_pinv = vecs * inv_vals @ vecs.conj().T
    return (H_pinv, P0)