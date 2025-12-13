from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

def _norm(psi: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12)