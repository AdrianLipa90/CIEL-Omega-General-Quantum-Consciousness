from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

class FeelingField:
    """
    Buduje przestrzenne pole afektywne z dwóch map:
      - intensity(x,y)  ∈ ℝ⁺
      - coherence(x,y)  ∈ [0,1]
    Zwraca: affect(x,y) ∈ [0,1]
    """
    gain: float = 1.0

    def build(self, intensity: np.ndarray, coherence: np.ndarray) -> np.ndarray:
        intensity = np.asarray(intensity, dtype=float)
        coherence = np.asarray(coherence, dtype=float)
        aff = np.tanh(self.gain * intensity * coherence)
        return np.clip(aff, 0.0, 1.0)