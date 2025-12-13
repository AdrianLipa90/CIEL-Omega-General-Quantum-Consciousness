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

class Observables:
    """Export do HDF5: I_abs2, tau, Lambda0 + logi ζ i R"""

    def __init__(self, out_path: str='ciel0_run.h5'):
        self.out_path = out_path

    def export(self, fs: FieldStack, extra: Dict[str, np.ndarray]):
        try:
            with h5py.File(self.out_path, 'w') as h:
                h['I_abs2'] = np.abs(fs.I) ** 2
                h['tau'] = fs.tau
                h['Lambda0'] = fs.L0
                for k, v in extra.items():
                    h[k] = v
        except Exception as e:
            print(f'Warning: Could not save observables: {e}')