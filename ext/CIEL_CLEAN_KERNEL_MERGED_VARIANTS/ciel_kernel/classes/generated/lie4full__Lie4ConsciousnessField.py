import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings

class Lie4ConsciousnessField:

    def __init__(self, spacetime_shape: Tuple[int, int, int, int], constants: Lie4Constants):
        self.C = constants
        self.shape = spacetime_shape
        self.I = np.zeros(spacetime_shape + (4,), dtype=np.complex128)
        self.J = np.zeros(spacetime_shape, dtype=np.complex128)
        self.A = np.zeros(spacetime_shape + (4, 4, 4), dtype=np.complex128)
        self._initialize_fields()

    def _initialize_fields(self):
        Nx, Ny, Nz, Nt = self.shape
        x, y, z, t = np.meshgrid(np.linspace(-1, 1, Nx), np.linspace(-1, 1, Ny), np.linspace(-1, 1, Nz), np.linspace(0, 2 * np.pi, Nt), indexing='ij')
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2 + 1e-08)
        self.I[..., 0] = np.exp(1j * 2 * np.pi * t) * np.exp(-r / 0.3)
        self.I[..., 1] = 0.5 * np.sin(2 * np.pi * x) * np.cos(2 * np.pi * y)
        self.I[..., 2] = 0.3 * np.exp(1j * 2 * np.pi * z)
        self.I[..., 3] = 0.8 * np.exp(-r / 0.25)
        self.J = np.exp(1j * 1.0 * (x + y + z)) * np.exp(-r / 0.35)
        for mu in range(4):
            phase = np.exp(1j * 0.3 * (mu + 0.5 * x + 0.3 * y))
            base = 0.05 * phase
            for i in range(4):
                self.A[..., mu, i, i] = base