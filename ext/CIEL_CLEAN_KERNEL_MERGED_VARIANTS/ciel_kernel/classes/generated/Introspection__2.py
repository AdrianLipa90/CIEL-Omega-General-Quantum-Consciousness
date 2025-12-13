from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class Introspection:
    low_thr: float = 0.3
    high_thr: float = 0.8

    def state(self, ego: np.ndarray, world: np.ndarray) -> Dict[str, float | str]:
        a = ego.real.ravel()
        b = world.real.ravel()
        a = (a - a.mean()) / (a.std() + 1e-12)
        b = (b - b.mean()) / (b.std() + 1e-12)
        rho = float(np.dot(a, b) / (len(a) - 1))
        st = 'integration' if rho > self.high_thr else 'dissociation' if rho < self.low_thr else 'mixed'
        return {'rho': rho, 'state': st}