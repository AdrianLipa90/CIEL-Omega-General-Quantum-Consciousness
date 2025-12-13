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

class FieldStack:
    """
    Intentional complex scalar I, aether vector Fμ, lambda scalar λ; diagnostics.
    """

    def __init__(self, grid: Grid):
        self.g = grid
        shape = (grid.nx, grid.ny, grid.nz, grid.nt)
        self.I = np.zeros(shape, dtype=np.complex128)
        self.F = np.zeros(shape + (4,), dtype=float)
        self.lam = np.zeros(shape, dtype=float)
        self.R = np.zeros(shape, dtype=float)
        self.mass = np.zeros(shape, dtype=float)
        self.L0 = np.zeros(shape, dtype=float)
        self.tau = np.zeros(shape, dtype=float)