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

def zeta_modulation(t: float, val: complex, I: np.ndarray, strength=0.01) -> np.ndarray:
    """Moduluje fazę i amplitudę pola I przez wartości ζ(s)"""
    phase = np.exp(1j * strength * np.real(val))
    amp = 1.0 + strength * np.imag(val)
    return I * phase * amp