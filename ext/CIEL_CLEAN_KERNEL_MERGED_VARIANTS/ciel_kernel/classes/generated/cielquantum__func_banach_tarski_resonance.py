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

def banach_tarski_resonance(I: np.ndarray, strength=0.05) -> np.ndarray:
    """Symboliczne rozszczepienie/sklejenie faz: permutacja bloków"""
    flat = I.flatten()
    rng = np.random.default_rng(123)
    idx = np.arange(flat.size)
    rng.shuffle(idx)
    flat2 = flat[idx]
    out = (1 - strength) * flat + strength * flat2
    return out.reshape(I.shape)