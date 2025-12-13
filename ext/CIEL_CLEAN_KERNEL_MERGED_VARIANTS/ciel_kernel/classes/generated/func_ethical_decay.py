from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

def ethical_decay(E: float, tau: float=0.05) -> float:
    """Redukcja 'napięcia etycznego' – model relaksacji energii moralnej."""
    return float(np.exp(-E * tau))