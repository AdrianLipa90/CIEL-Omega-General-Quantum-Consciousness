from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class QuantumOptimiser:
    lr: float = 0.05
    steps: int = 50
    ethical_weight: float = 1.0

    def optimize_constants(self, constants: Dict[str, float], metrics_fn: Callable[[Dict[str, float]], Tuple[float, float, bool]]) -> Dict[str, float]:
        keys = list(constants.keys())
        for _ in range(self.steps):
            coh, fid, ok = metrics_fn(constants)
            loss = (1 - coh) ** 2 + (1 - fid) ** 2 + (0 if ok else 0.1 * self.ethical_weight)
            grad = {}
            eps = 0.001
            for k in keys:
                orig = constants[k]
                constants[k] = orig + eps
                coh2, fid2, ok2 = metrics_fn(constants)
                loss2 = (1 - coh2) ** 2 + (1 - fid2) ** 2 + (0 if ok2 else 0.1 * self.ethical_weight)
                grad[k] = (loss2 - loss) / eps
                constants[k] = orig
            for k in keys:
                constants[k] -= self.lr * grad[k]
        return constants