from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class OmegaDriftCorePlus:
    clock: SchumannClock
    drift_gain: float = 0.045
    harmonic_sweep: Tuple[int, int] = (1, 3)
    jitter: float = 0.004
    renorm: bool = True

    def step(self, psi: np.ndarray, sigma_scalar: float=1.0, t: Optional[float]=None) -> np.ndarray:
        hmin, hmax = self.harmonic_sweep
        h = int(np.clip(round(hmin + (hmax - hmin) * np.clip(sigma_scalar, 0, 1)), hmin, hmax))
        ph = self.clock.phase(k=h, at=t) + np.random.uniform(-self.jitter, self.jitter)
        psi = psi * np.exp(1j * (self.drift_gain * sigma_scalar + ph))
        if self.renorm:
            psi /= _norm(psi)
        return psi