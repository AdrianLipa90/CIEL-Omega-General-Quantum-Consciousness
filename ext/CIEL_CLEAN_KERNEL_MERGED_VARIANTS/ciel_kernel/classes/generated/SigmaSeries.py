from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import numpy as np

class SigmaSeries:
    alpha: float = 0.618
    sigma0: float = 0.42
    steps: int = 256

    def run(self) -> np.ndarray:
        t = np.arange(self.steps, dtype=float)
        a_pow = self.alpha ** t
        sigma = np.empty(self.steps, dtype=float)
        s = float(self.sigma0)
        for i in range(self.steps):
            s = s + a_pow[i] * (1.0 - s)
            sigma[i] = s
        return sigma

    def apply_to_field(self, field: np.ndarray) -> np.ndarray:
        """
        Zastosuj ostatnią wartość Σ_T jako delikatną normalizację amplitudy pola.
        Bez FFT: wyłącznie skalowanie, stabilne numerycznie.
        """
        sigma_T = float(self.run()[-1])
        amp = np.sqrt(np.mean(np.abs(field) ** 2)) + 1e-12
        target = np.sqrt(sigma_T)
        return field * (target / amp)