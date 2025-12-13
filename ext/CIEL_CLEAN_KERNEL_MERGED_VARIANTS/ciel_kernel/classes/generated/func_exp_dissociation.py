from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def exp_dissociation() -> Dict[str, Any]:
    """Korelacja ego↔świat (dissociation vs integration)."""
    ego, _, _ = make_seed()
    world = np.roll(ego, 3, axis=0) * np.exp(1j * 0.2)
    a = ego.real.ravel()
    b = world.real.ravel()
    a = (a - a.mean()) / (a.std() + 1e-12)
    b = (b - b.mean()) / (b.std() + 1e-12)
    rho = float(np.dot(a, b) / (len(a) - 1))
    state = 'integration' if rho > 0.8 else 'dissociation' if rho < 0.3 else 'mixed'
    return {'rho': rho, 'state': state}