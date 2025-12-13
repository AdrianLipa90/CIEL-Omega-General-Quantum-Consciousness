from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class RCDECalibratorPro:
    lam: float = 0.22
    dt: float = 0.05
    sigma: float = 0.5
    lam_bounds: Tuple[float, float] = (0.05, 0.5)

    def step(self, psi: np.ndarray) -> float:
        target = float(_norm(psi) ** 2)
        err = target - self.sigma
        lam_adapt = float(np.clip(self.lam * (1 + 0.8 * abs(err)), *self.lam_bounds))
        self.sigma = float(np.clip(self.sigma + self.dt * lam_adapt * err, 0.0, 1.5))
        return self.sigma