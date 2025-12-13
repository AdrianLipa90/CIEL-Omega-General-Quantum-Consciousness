from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np

class UnifiedSigmaField:
    shape: Tuple[int, int] = (128, 128)
    omega: float = 0.7
    damping: float = 0.02
    radial_scale: float = 1.4
    dt: float = 0.05
    sigma_t: float = field(init=False, default=0.5)

    def __post_init__(self):
        pass

    def _base_spatial(self) -> np.ndarray:
        H, W = self.shape
        y = np.linspace(-1.0, 1.0, H)[:, None]
        x = np.linspace(-1.0, 1.0, W)[None, :]
        r2 = (x ** 2 + y ** 2) / self.radial_scale ** 2
        return np.exp(-r2)

    def step(self, t: float, prev_sigma: Optional[float]=None) -> Tuple[np.ndarray, float]:
        """
        Zwraca: (Σ_field_t, Σ_scalar_t)
        - Σ_field_t: przestrzenny rozkład Σ w chwili t
        - Σ_scalar_t: skalarna koherencja (uśredniona), użyteczna do normalizacji pól
        """
        if prev_sigma is None:
            prev_sigma = self.sigma_t
        temporal = np.exp(-self.damping * t) * np.cos(self.omega * t)
        sigma_scalar = 0.5 * (1.0 + temporal)
        s = 0.85 * prev_sigma + 0.15 * sigma_scalar
        self.sigma_t = float(np.clip(s, 0.0, 1.0))
        spatial = self._base_spatial()
        sigma_field = self.sigma_t * spatial
        return (sigma_field.astype(np.float64, copy=False), self.sigma_t)

    def evolve(self, T: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generuje przebieg Σ(x,t) i Σ̄(t) dla t=0..T-1.
        Zwraca (fields, scalars):
          fields  : [T, H, W]
          scalars : [T]
        """
        H, W = self.shape
        fields = np.zeros((T, H, W), dtype=np.float64)
        scalars = np.zeros((T,), dtype=np.float64)
        prev = self.sigma_t
        for i in range(T):
            field, prev = self.step(t=i * self.dt, prev_sigma=prev)
            fields[i] = field
            scalars[i] = prev
        return (fields, scalars)