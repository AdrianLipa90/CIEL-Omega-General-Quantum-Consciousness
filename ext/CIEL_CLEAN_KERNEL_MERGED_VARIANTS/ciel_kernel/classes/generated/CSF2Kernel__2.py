from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class CSF2Kernel:
    dt: float = 0.05
    k_psi: float = 0.8
    k_sigma: float = 0.6
    k_couple: float = 0.5
    k_world: float = 0.2

    def step(self, s: CSF2State) -> CSF2State:
        dpsi = 1j * self.k_psi * _lap(s.psi) + self.k_couple * (s.lam * s.sigma - s.omega * s.psi)
        dsig = self.k_sigma * (np.abs(s.psi) ** 2 - s.sigma) - 0.1 * s.sigma ** 2
        dome = 0.05 * _lap(s.omega) - 0.02 * (s.omega - np.mean(s.omega))
        dlam = 0.1 * (s.psi * np.conj(s.psi)) - 0.05 * s.lam
        psi2 = s.psi + self.dt * dpsi
        psi2 = psi2 / (_norm(psi2) + 1e-12)
        sigma2 = np.clip(s.sigma + self.dt * dsig, 0.0, 2.0)
        omega2 = s.omega + self.dt * dome
        lambda_2 = s.lam + self.dt * dlam
        return CSF2State(psi2, sigma2, lambda_2, omega2)