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

def resonance(S: np.ndarray, I: np.ndarray) -> np.ndarray:
    if S.ndim == I.ndim:
        num = np.abs(np.conj(S) * I) ** 2
        den = ((np.abs(S) + 1e-15) * (np.abs(I) + 1e-15)) ** 2
    else:
        num = np.abs(np.sum(np.conj(S) * I, axis=-1)) ** 2
        den = (np.linalg.norm(S, axis=-1) * np.linalg.norm(I, axis=-1) + 1e-15) ** 2
    return num / den