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

class StableEvolver:

    def __init__(self, phys: CIELPhysics, grid: Grid, fields: FieldStack):
        self.ph = phys
        self.g = grid
        self.fs = fields
        self.dx, self.dy, self.dz, self.dt = grid.steps()
        self.dt = min(self.dt, self.ph.cfl_safety * min(self.dx, self.dy, self.dz) / self.ph.c)

    def absorbing_bc(self, arr: np.ndarray, alpha=0.02):
        """Sponge layers na brzegach 3D"""
        for ax, n in enumerate([self.g.nx, self.g.ny, self.g.nz]):
            sl = [slice(None)] * arr.ndim
            sl[ax] = slice(0, 2)
            arr[tuple(sl)] *= 1 - alpha
            sl[ax] = slice(n - 2, n)
            arr[tuple(sl)] *= 1 - alpha
        return arr

    def step_I(self):
        """Evolve intention field I"""
        I = self.fs.I
        lap = sum((np.gradient(np.gradient(I, axis=ax), axis=ax) for ax in range(3)))
        t2 = np.gradient(np.gradient(I, axis=3), axis=3) / self.ph.c ** 2
        nonlin = 2 * self.ph.lambda_1 * np.abs(I) ** 2 * I
        phase_term = 1j * self.ph.lambda_3 * np.sin(self.fs.tau - np.angle(I)) / np.maximum(np.abs(I), 1e-12) * I
        dIdt = -(lap + t2 + nonlin + phase_term)
        I_next = I + self.dt * dIdt
        self.fs.I = self.absorbing_bc(I_next)

    def step_tau(self):
        """Evolve temporal field τ"""
        tau = self.fs.tau
        grad_list = [np.gradient(tau, axis=ax) for ax in range(4)]
        rho = sum((g ** 2 for g in grad_list))
        f_rho = 1.0 / (2 * (1 + rho ** 2))
        div_term = 0.0
        for ax in range(4):
            div_term += np.gradient(f_rho * np.gradient(tau, axis=ax), axis=ax)
        phase_term = self.ph.lambda_3 * np.sin(tau - np.angle(self.fs.I))
        dtau = div_term - phase_term
        self.fs.tau = self.absorbing_bc(tau + self.dt * dtau)