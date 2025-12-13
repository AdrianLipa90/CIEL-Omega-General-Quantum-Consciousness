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

def enforce_ethics(R: np.ndarray, threshold: float, I: np.ndarray) -> Tuple[np.ndarray, bool]:
    avg = float(np.mean(R))
    if avg < threshold:
        scale = np.sqrt(threshold / max(avg, 1e-12))
        return (I * scale, False)
    return (I, True)