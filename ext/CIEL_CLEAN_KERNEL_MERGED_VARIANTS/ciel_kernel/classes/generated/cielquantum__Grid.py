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

class Grid:
    """3D+1 spacetime grid"""
    nx: int = 32
    ny: int = 32
    nz: int = 32
    nt: int = 64
    Lx: float = 1.0
    Ly: float = 1.0
    Lz: float = 1.0
    T: float = 1.0

    def steps(self):
        dx = self.Lx / self.nx
        dy = self.Ly / self.ny
        dz = self.Lz / self.nz
        dt = self.T / self.nt
        return (dx, dy, dz, dt)