from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class PredictiveCore:
    tau: float = 12.0

    def predict(self, history: List[float]) -> float:
        if not history:
            return 0.0
        h = np.asarray(history, dtype=float)
        t = np.arange(len(h))[::-1]
        w = np.exp(-t / max(self.tau, 1e-06))
        return float(np.sum(w * h) / (np.sum(w) + 1e-12))