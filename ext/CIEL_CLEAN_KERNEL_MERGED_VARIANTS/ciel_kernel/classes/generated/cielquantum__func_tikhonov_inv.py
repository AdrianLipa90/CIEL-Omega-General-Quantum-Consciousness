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

def tikhonov_inv(A, lam=1e-10):
    """(A^†A + λI)^-1 A^†"""
    U, s, Vh = la.svd(A, full_matrices=False)
    s_f = s / (s ** 2 + lam)
    return Vh.conj().T * s_f @ U.conj().T