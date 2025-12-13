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

class QFTSystem:
    """
    Canonical fields, Lagrangian density, conjugate momenta, gauge-fixing (R_ξ), ghosts, propagators, 1-step RG.
    """

    def __init__(self, phys: CIELPhysics, grid: Grid, fields: FieldStack):
        self.ph = phys
        self.g = grid
        self.fs = fields

    def lagrangian_density(self, I, F, lam):
        """Uproszczona lokalna L: |∂I|^2 - m_I^2|I|^2 - λ1|I|^4 + (1/4)F_{μν}F^{μν} + (1/2)(∂λ)^2 - V(λ) + gλ F·F"""
        grad_I2 = sum((np.abs(np.gradient(I, axis=ax)) ** 2 for ax in (0, 1, 2)))
        time_I2 = np.abs(np.gradient(I, axis=3)) ** 2 / self.ph.c ** 2
        LI = grad_I2.sum() + time_I2.sum() - self.ph.mp ** 2 * (np.abs(I) ** 2).sum() - self.ph.lambda_1 * (np.abs(I) ** 4).sum()
        divF = sum((np.gradient(F[..., mu], axis=mu if mu < 3 else 3) for mu in range(4)))
        curlF2 = 0.0
        for a in range(4):
            for b in range(a + 1, 4):
                curlF2 += np.sum((np.gradient(F[..., b], axis=a) - np.gradient(F[..., a], axis=b)) ** 2)
        LF = 0.25 * curlF2 - 0.5 * (divF ** 2).sum()
        grad_l2 = sum(((np.gradient(lam, axis=ax) ** 2).sum() for ax in range(4)))
        Vlam = 0.5 * self.ph.lambda_2 * (lam ** 2).sum()
        Lint = self.ph.beta * ((divF ** 2).sum() - curlF2) + self.ph.lambda_2 * np.sum(lam * np.sum(F ** 2, axis=-1))
        return LI + LF + 0.5 * grad_l2 - Vlam + Lint

    def conjugate_momenta(self, I):
        """π_I ≈ ∂_t I / c^2 (uproszczenie)"""
        pi_I = np.gradient(I, axis=3) / self.ph.c ** 2
        return pi_I

    def gauge_fixing(self, F):
        """R_ξ: L_gf = -(1/2ξ) (∂_μ F^μ)^2"""
        divF = sum((np.gradient(F[..., mu], axis=mu if mu < 3 else 3) for mu in range(4)))
        return -(1.0 / (2 * self.ph.xi)) * np.sum(divF ** 2)

    def ghost_action(self, F_shape):
        """Placeholder for ghost terms"""
        return 0.0

    def propagator(self, K: np.ndarray, scheme='tikhonov'):
        n = K.shape[0]
        if scheme == 'tikhonov':
            return tikhonov_inv(K.reshape(n, n)).reshape(K.shape)
        elif scheme == 'pseudoinv':
            Kp, _ = remove_zero_modes((K + K.conj().transpose()) / 2)
            return Kp
        else:
            return la.pinvh((K + K.conj().T) / 2)

    def rg_step(self, g: float, b0=11 / 12, b1=17 / 24, dlogμ=0.1):
        """1-loop-like β(g) = -b0 g^3 + b1 g^5"""
        beta = -b0 * g ** 3 + b1 * g ** 5
        return g + beta * dlogμ