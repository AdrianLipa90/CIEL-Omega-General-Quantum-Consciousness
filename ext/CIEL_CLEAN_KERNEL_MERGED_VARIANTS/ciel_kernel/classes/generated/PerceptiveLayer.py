from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class PerceptiveLayer:
    clip_percentile: Optional[float] = 99.5

    def compute(self, psi_field: np.ndarray, sigma_field: np.ndarray) -> np.ndarray:
        psi = psi_field.astype(np.complex128, copy=False)
        sig = sigma_field.astype(np.float64, copy=False)
        percept = sig * (psi.real + np.abs(psi.imag))
        if self.clip_percentile is not None:
            hi = np.percentile(percept, self.clip_percentile)
            percept = np.clip(percept, 0.0, hi) / (hi + 1e-12)
        else:
            percept = percept / (np.max(percept) + 1e-12)
        return percept