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

def emergent_mass(mu0: float, R: np.ndarray) -> np.ndarray:
    m2 = mu0 * (1.0 - R)
    return np.sqrt(np.maximum(m2, 0.0))