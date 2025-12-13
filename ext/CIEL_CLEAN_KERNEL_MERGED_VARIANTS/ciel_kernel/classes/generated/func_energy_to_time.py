from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

def energy_to_time(E: float, h: float=6.62607015e-34) -> float:
    """Konwersja energii do czasu w wymiarze etycznym."""
    return h / (E + 1e-12)