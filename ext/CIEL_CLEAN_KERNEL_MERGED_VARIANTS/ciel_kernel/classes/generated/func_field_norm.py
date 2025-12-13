from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def field_norm(psi: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12)