import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special, ndimage
from scipy.interpolate import RectBivariateSpline
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings
import numpy.typing as npt
from sympy import isprime

class UnifiedSevenFundamentalFields:

    def __init__(self, constants: UnifiedCIELConstants, spacetime_shape: tuple):
        self.C = constants
        self.spacetime_shape = spacetime_shape
        self.psi = np.zeros(spacetime_shape, dtype=np.complex128)
        self.I_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.zeta_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.sigma_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.g_metric = np.zeros(spacetime_shape + (4, 4), dtype=np.float64)
        self.M_field = np.zeros(spacetime_shape + (3,), dtype=np.complex128)
        self.G_info = np.zeros(spacetime_shape + (2, 2), dtype=np.float64)
        self.ramanujan_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.schrodinger_4d_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.ramanujan_4d_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.collatz_4d_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.riemann_4d_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self.banach_tarski_4d_field = np.zeros(spacetime_shape, dtype=np.complex128)
        self._initialize_fields_vectorized()

    def _initialize_fields_vectorized(self):
        nx, ny, nt = self.spacetime_shape
        x, y, t = np.meshgrid(np.linspace(-1, 1, nx), np.linspace(-1, 1, ny), np.linspace(0, 2 * np.pi, nt), indexing='ij')
        r = np.sqrt(x ** 2 + y ** 2 + 1e-10)
        theta = np.arctan2(y, x)
        self.I_field = np.exp(1j * theta) * np.exp(-r / 0.3)
        self.psi = 0.5 * np.exp(1j * 2.0 * x) * np.exp(-r / 0.4)
        self.sigma_field = np.exp(1j * theta)
        self.zeta_field = 0.1 * np.exp(1j * 0.5 * t) * np.sin(1.0 * x)
        for i in range(nx):
            for j in range(ny):
                tau = complex(x[i, j, 0], 0.1 + abs(y[i, j, 0]))
                self.ramanujan_field[i, j, :] = EnhancedMathematicalStructure.ramanujan_modular_forms(tau) * 1e-06
        self._initialize_metric_vectorized()
        self._initialize_information_geometry()

    def _initialize_metric_vectorized(self):
        g_minkowski = np.diag([1.0, -1.0, -1.0, -1.0])
        self.g_metric[:] = g_minkowski
        I_magnitude = np.abs(self.I_field)[..., np.newaxis, np.newaxis]
        perturbation = 0.01 * I_magnitude * np.ones((4, 4))
        for i in range(4):
            perturbation[..., i, i] = 0.0
        self.g_metric += perturbation

    def _initialize_information_geometry(self):
        nx, ny, nt = self.spacetime_shape
        x, y, t = np.meshgrid(np.linspace(0, 2 * np.pi, nx), np.linspace(0, 2 * np.pi, ny), np.linspace(0, 2 * np.pi, nt), indexing='ij')
        self.G_info[..., 0, 0] = 1.0 + 0.1 * np.sin(0.5 * x)
        self.G_info[..., 1, 1] = 1.0 + 0.1 * np.cos(0.5 * y)
        self.G_info[..., 0, 1] = 0.05 * np.sin(0.5 * (x + y))
        self.G_info[..., 1, 0] = self.G_info[..., 0, 1]

    def update_from_4d_engine(self, engine_4d: UniversalLawEngine4D):
        """Project 4D engine fields to 3D spacetime - FIXED SCALING"""
        try:

            def safe_projection_4d_to_2d(field_4d):
                field_2d = np.mean(field_4d, axis=(2, 3))
                norm_4d = np.linalg.norm(field_4d)
                norm_2d = np.linalg.norm(field_2d)
                if norm_2d > 1e-10:
                    field_2d *= norm_4d / norm_2d * 0.5
                return field_2d
            symbolic_2d = safe_projection_4d_to_2d(engine_4d.symbolic_field)
            intention_2d = safe_projection_4d_to_2d(engine_4d.intention_field)
            resonance_2d = safe_projection_4d_to_2d(engine_4d.resonance_field)
            creation_2d = safe_projection_4d_to_2d(engine_4d.creation_field)

            def safe_resize(field_2d, target_shape):
                if field_2d.shape[0] == 0 or field_2d.shape[1] == 0:
                    return np.zeros(target_shape, dtype=field_2d.dtype)
                zoom_factors = [target_shape[0] / field_2d.shape[0], target_shape[1] / field_2d.shape[1]]
                if any((z <= 0 or z > 100 for z in zoom_factors)):
                    x_old = np.linspace(0, 1, field_2d.shape[0])
                    y_old = np.linspace(0, 1, field_2d.shape[1])
                    x_new = np.linspace(0, 1, target_shape[0])
                    y_new = np.linspace(0, 1, target_shape[1])
                    if np.iscomplexobj(field_2d):
                        real_interp = RectBivariateSpline(x_old, y_old, field_2d.real)
                        imag_interp = RectBivariateSpline(x_old, y_old, field_2d.imag)
                        result = real_interp(x_new, y_new) + 1j * imag_interp(x_new, y_new)
                    else:
                        interp = RectBivariateSpline(x_old, y_old, field_2d)
                        result = interp(x_new, y_new)
                else:
                    result = ndimage.zoom(field_2d, zoom_factors, order=1)
                norm_before = np.linalg.norm(field_2d)
                norm_after = np.linalg.norm(result)
                if norm_after > 1e-10:
                    result *= norm_before / norm_after
                return result
            target_shape = self.spacetime_shape[:2]
            symbolic_resized = safe_resize(symbolic_2d, target_shape)
            intention_resized = safe_resize(intention_2d, target_shape)
            resonance_resized = safe_resize(resonance_2d, target_shape)
            creation_resized = safe_resize(creation_2d, target_shape)

            def safe_exp(arg, max_arg=50):
                arg_clipped = np.clip(np.real(arg), -max_arg, max_arg)
                if np.iscomplexobj(arg):
                    imag_part = np.imag(arg)
                    return np.exp(arg_clipped) * np.exp(1j * imag_part)
                return np.exp(arg_clipped)

            def normalize_field(field, target_max=1.0):
                field_max = np.max(np.abs(field))
                if field_max > 1e-10:
                    return field * (target_max / field_max)
                return field
            symbolic_resized = normalize_field(symbolic_resized, 1.0)
            intention_resized = normalize_field(intention_resized, 1.0)
            resonance_resized = normalize_field(resonance_resized, 1.0)
            creation_resized = normalize_field(creation_resized, 1.0)
            alpha = 0.3
            for t_idx in range(self.spacetime_shape[2]):
                time_phase = 0.1 * t_idx
                time_factor = safe_exp(1j * time_phase)
                self.schrodinger_4d_field[:, :, t_idx] = symbolic_resized * time_factor
                self.ramanujan_4d_field[:, :, t_idx] = intention_resized * safe_exp(1j * 0.05 * t_idx)
                self.collatz_4d_field[:, :, t_idx] = resonance_resized * safe_exp(1j * 0.02 * t_idx)
                self.riemann_4d_field[:, :, t_idx] = np.abs(symbolic_resized) * safe_exp(1j * 0.03 * t_idx)
                self.banach_tarski_4d_field[:, :, t_idx] = creation_resized * safe_exp(1j * 0.04 * t_idx)
                self.psi[:, :, t_idx] = (1 - alpha) * self.psi[:, :, t_idx] + alpha * symbolic_resized
                self.I_field[:, :, t_idx] = (1 - alpha) * self.I_field[:, :, t_idx] + alpha * intention_resized
            self.psi = normalize_field(self.psi, 1.0)
            self.I_field = normalize_field(self.I_field, 1.0)
        except Exception as e:
            print(f'Warning in update_from_4d_engine: {e}')
            import traceback
            traceback.print_exc()