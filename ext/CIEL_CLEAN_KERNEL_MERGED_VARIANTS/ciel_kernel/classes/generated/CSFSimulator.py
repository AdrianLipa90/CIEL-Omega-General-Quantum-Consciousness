from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class CSFSimulator:
    size: int = 128
    sigma: float = 2.0
    dt: float = 0.01
    smooth_strength: float = 0.15
    seed: Optional[int] = None
    X: np.ndarray = field(init=False, repr=False)
    Y: np.ndarray = field(init=False, repr=False)
    psi: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        if self.seed is not None:
            np.random.seed(self.seed)
        x = np.linspace(-3.0, 3.0, self.size)
        y = np.linspace(-3.0, 3.0, self.size)
        self.X, self.Y = np.meshgrid(x, y)
        env = np.exp(-(self.X ** 2 + self.Y ** 2) / self.sigma ** 2)
        phase = np.exp(1j * (self.X + self.Y))
        self.psi = env * phase

    @staticmethod
    def _smooth2d(a: np.ndarray, k: int=1) -> np.ndarray:
        """prosty filtr pudełkowy – bez FFT"""
        if k <= 0:
            return a
        out = a.copy()
        for _ in range(k):
            tmp = np.pad(out, ((1, 1), (1, 1)), mode='reflect')
            out = (tmp[1:-1, 1:-1] + tmp[0:-2, 1:-1] + tmp[2:, 1:-1] + tmp[1:-1, 0:-2] + tmp[1:-1, 2:]) / 5.0
        return out

    def step(self, n: int=1, drift: float=1.0) -> None:
        """Iteracyjna ewolucja w domenie realnej."""
        for _ in range(n):
            gy = np.zeros_like(self.psi)
            gx = np.zeros_like(self.psi)
            gy[1:-1, :] = 0.5 * (self.psi[2:, :] - self.psi[:-2, :])
            gx[:, 1:-1] = 0.5 * (self.psi[:, 2:] - self.psi[:, :-2])
            self.psi += 1j * self.dt * drift * (gy + gx)
            s_real = self._smooth2d(self.psi.real)
            s_imag = self._smooth2d(self.psi.imag)
            self.psi = (1 - self.smooth_strength) * self.psi + self.smooth_strength * (s_real + 1j * s_imag)
            self.psi /= np.sqrt(np.mean(np.abs(self.psi) ** 2)) + 1e-12