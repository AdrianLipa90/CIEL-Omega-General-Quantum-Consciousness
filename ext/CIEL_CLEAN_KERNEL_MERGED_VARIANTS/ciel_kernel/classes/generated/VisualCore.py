from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import numpy as np

class VisualCore:
    """
    Nie rysuje – tylko przygotowuje dane wizualne (H×W×C) do dalszego użycia.
    Kanały:
      0: amplitude (|ψ|)
      1: phase_sin (sin(arg ψ))
      2: phase_cos (cos(arg ψ))
    """
    clip_amp: Optional[float] = None

    def tensorize(self, psi: np.ndarray) -> np.ndarray:
        amp = np.abs(psi)
        if self.clip_amp is not None:
            hi = np.percentile(amp, self.clip_amp)
            amp = np.clip(amp, 0.0, hi) / (hi + 1e-12)
        else:
            amp = amp / (np.max(amp) + 1e-12)
        ph = np.angle(psi)
        ph_s = np.sin(ph)
        ph_c = np.cos(ph)
        return np.stack([amp, ph_s, ph_c], axis=-1)