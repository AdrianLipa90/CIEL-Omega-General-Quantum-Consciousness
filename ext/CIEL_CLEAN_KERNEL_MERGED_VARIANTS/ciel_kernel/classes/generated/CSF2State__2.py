from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class CSF2State:
    psi: np.ndarray
    sigma: np.ndarray
    lam: np.ndarray
    omega: np.ndarray

    def clone(self) -> 'CSF2State':
        return CSF2State(self.psi.copy(), self.sigma.copy(), self.lam.copy(), self.omega.copy())