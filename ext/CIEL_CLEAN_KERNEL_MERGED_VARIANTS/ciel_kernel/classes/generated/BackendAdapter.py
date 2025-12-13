from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class BackendAdapter:
    """
    Oczekuje backendu z metodami:
      - set_fields(psi: np.ndarray, sigma: np.ndarray)
      - step(dt: float) -> None
      - get_fields() -> Tuple[np.ndarray, np.ndarray]
    Jeśli ich nie ma – działa tryb awaryjny (wewnętrzny CSF2Kernel).
    """

    def __init__(self, backend: Optional[Any]=None, grid_size: int=96):
        self._fallback_kernel = CSF2Kernel(dt=0.02)
        self._fallback_state: Optional[Tuple[np.ndarray, np.ndarray]] = None
        self.backend = backend
        self.grid_size = grid_size
        if self.backend is None:
            x = np.linspace(-2, 2, grid_size)
            y = np.linspace(-2, 2, grid_size)
            X, Y = np.meshgrid(x, y)
            psi = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.2 * Y))
            psi /= _norm(psi) + 1e-12
            sigma = np.exp(-(X ** 2 + Y ** 2) / 2.0)
            self._fallback_state = (psi.astype(np.complex128), sigma.astype(np.float64))

    def set_fields(self, psi: np.ndarray, sigma: np.ndarray) -> None:
        if self.backend is not None and hasattr(self.backend, 'set_fields'):
            self.backend.set_fields(psi, sigma)
        else:
            self._fallback_state = (psi.copy(), sigma.copy())

    def step(self, dt: float) -> None:
        if self.backend is not None and hasattr(self.backend, 'step'):
            self.backend.step(dt=dt)
        else:
            if self._fallback_state is None:
                return
            psi, sigma = self._fallback_state
            s = CSF2State(psi, sigma, np.ones_like(psi) * 0.1, np.zeros_like(sigma))
            self._fallback_kernel.dt = dt
            s2 = self._fallback_kernel.step(s)
            self._fallback_state = (s2.psi, s2.sigma)

    def get_fields(self) -> Tuple[np.ndarray, np.ndarray]:
        if self.backend is not None and hasattr(self.backend, 'get_fields'):
            return self.backend.get_fields()
        else:
            assert self._fallback_state is not None
            return self._fallback_state