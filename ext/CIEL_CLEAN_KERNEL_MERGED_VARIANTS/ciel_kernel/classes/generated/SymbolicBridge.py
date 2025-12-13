from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

class SymbolicBridge:
    """Integruje glyphy z ColorOS i Σ (no-FFT)."""
    sigma_scalar: float
    palette: Dict[str, Tuple[float, float, float]] = field(default_factory=lambda: {'SOUL_BLUE': (0.2, 0.4, 0.9), 'INTENTION_GOLD': (0.95, 0.8, 0.2), 'ETHICS_WHITE': (1.0, 1.0, 0.95), 'WARNING_RED': (0.9, 0.2, 0.2), 'BALANCE_GREEN': (0.3, 0.9, 0.5)})

    def glyph_color(self, coherence: float) -> Tuple[float, float, float]:
        """Łączy Σ z koherencją glyphu i zwraca kolor RGB."""
        val = np.clip(coherence * self.sigma_scalar, 0.0, 1.0)
        if val < 0.3:
            base = np.array(self.palette['WARNING_RED'])
        elif val < 0.7:
            base = np.array(self.palette['INTENTION_GOLD'])
        else:
            base = np.array(self.palette['ETHICS_WHITE'])
        return tuple(base * val + (1 - val) * np.array(self.palette['SOUL_BLUE']))