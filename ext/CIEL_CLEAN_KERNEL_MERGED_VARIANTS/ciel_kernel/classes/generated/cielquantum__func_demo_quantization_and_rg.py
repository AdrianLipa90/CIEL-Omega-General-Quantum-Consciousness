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

def demo_quantization_and_rg():
    """Demo kwantyzacji i RG"""
    n = 64
    K = np.diag(2 * np.ones(n)) + np.diag(-1 * np.ones(n - 1), 1) + np.diag(-1 * np.ones(n - 1), -1)
    K[0, 0] = 1e-12
    Kp, P0 = remove_zero_modes(K, tol=1e-10, fudge=1e-08)
    phys = CIELPhysics()
    g0 = 0.1
    qft = QFTSystem(phys, Grid(), FieldStack(Grid()))
    g1 = qft.rg_step(g0, dlogμ=0.1)
    return (np.linalg.norm(Kp), np.trace(P0), g0, g1)