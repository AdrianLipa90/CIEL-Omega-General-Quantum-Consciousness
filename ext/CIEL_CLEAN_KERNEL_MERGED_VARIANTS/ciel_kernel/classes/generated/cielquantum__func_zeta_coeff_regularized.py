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

def zeta_coeff_regularized(tn, zeta_val, delta=0.3, eps=1e-12):
    denom = 1.0 + np.abs(tn) ** (1.0 + delta)
    coeff = zeta_val / denom
    coeff += eps * np.sign(coeff.real + 1j * coeff.imag)
    return coeff