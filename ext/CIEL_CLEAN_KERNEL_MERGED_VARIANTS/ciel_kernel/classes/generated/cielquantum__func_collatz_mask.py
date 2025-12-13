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

def collatz_mask(shape, steps: int=50) -> np.ndarray:
    """Maska rezonansowa: długość sekwencji Collatza do 1 dla indeksu liniowego"""
    mask = np.zeros(shape, dtype=float)
    flat = mask.reshape(-1)
    for i in range(flat.size):
        n = i + 1
        length = 0
        while n != 1 and length < steps:
            n = 3 * n + 1 if n % 2 else n // 2
            length += 1
        flat[i] = length
    mmax = np.max(flat)
    if mmax > 0:
        flat /= mmax
    return mask