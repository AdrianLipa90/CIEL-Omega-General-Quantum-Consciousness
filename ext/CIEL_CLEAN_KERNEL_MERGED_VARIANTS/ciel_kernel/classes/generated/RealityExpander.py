from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np

class RealityExpander:
    alpha: float = 0.6
    kappa: float = 0.12
    steps: int = 16
    preserve_norm: bool = True

    def _laplacian(self, a: np.ndarray) -> np.ndarray:
        out = np.zeros_like(a, dtype=a.dtype)
        out[1:-1, 1:-1] = a[2:, 1:-1] + a[:-2, 1:-1] + a[1:-1, 2:] + a[1:-1, :-2] - 4.0 * a[1:-1, 1:-1]
        return out

    def expand(self, seed_field: np.ndarray) -> np.ndarray:
        """
        Rozszerza pole przez (i) nieliniową transformację gradientową,
        (ii) lekką dyfuzję, (iii) (opcjonalnie) renormalizację amplitudy.
        """
        psi = seed_field.astype(np.complex128, copy=True)
        for _ in range(self.steps):
            gy = np.zeros_like(psi)
            gx = np.zeros_like(psi)
            gy[1:-1, :] = 0.5 * (psi[2:, :] - psi[:-2, :])
            gx[:, 1:-1] = 0.5 * (psi[:, 2:] - psi[:, :-2])
            grad_mag = np.sqrt(np.abs(gx) ** 2 + np.abs(gy) ** 2)
            growth = np.tanh(self.alpha * grad_mag) * np.exp(1j * np.angle(psi))
            diff = self._laplacian(psi)
            psi = psi + growth + self.kappa * diff
            if self.preserve_norm:
                psi /= np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12
        return psi