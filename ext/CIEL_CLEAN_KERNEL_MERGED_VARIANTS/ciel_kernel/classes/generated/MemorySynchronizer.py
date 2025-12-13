from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class MemorySynchronizer:
    alpha: float = 0.92
    beta: float = 0.08
    ms: Optional[np.ndarray] = None

    def update(self, sigma: np.ndarray, psi: np.ndarray) -> np.ndarray:
        if self.ms is None:
            self.ms = sigma.copy()
        self.ms = self.alpha * self.ms + self.beta * np.abs(psi)
        return self.ms