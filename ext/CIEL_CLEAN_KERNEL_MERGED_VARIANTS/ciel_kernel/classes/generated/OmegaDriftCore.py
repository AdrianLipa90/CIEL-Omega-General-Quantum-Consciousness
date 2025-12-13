from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

class OmegaDriftCore:
    clock: SchumannClock
    drift_gain: float = 0.05
    harmonic: int = 1
    renorm: bool = True

    def step(self, psi: np.ndarray, sigma_scalar: float=1.0) -> np.ndarray:
        carrier = self.clock.carrier(psi.shape, amp=1.0, k=self.harmonic)
        psi_next = psi * np.exp(1j * self.drift_gain * sigma_scalar) * carrier
        if self.renorm:
            psi_next /= field_norm(psi_next)
        return psi_next