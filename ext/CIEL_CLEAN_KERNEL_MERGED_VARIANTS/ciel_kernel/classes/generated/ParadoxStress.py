from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List
import numpy as np, json, math

class ParadoxStress:
    strength: float = 0.1

    def apply(self, s: CSF2State) -> CSF2State:
        jitter = (np.random.rand(*s.psi.shape) - 0.5) * self.strength
        s_new = s.clone()
        s_new.psi = s.psi * np.exp(1j * jitter)
        return s_new