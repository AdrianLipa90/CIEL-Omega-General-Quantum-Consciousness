from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def exp_noweparadoxy() -> Dict[str, Any]:
    """Stres test sensu – kontrolowany chaos decyzji."""
    val = random.random()
    paradox = 1 - val if random.random() > 0.5 else val
    vals = [random.random() for _ in range(9)]
    med = float(np.median(vals))
    return {'paradox_out': paradox, 'median_noise': med}