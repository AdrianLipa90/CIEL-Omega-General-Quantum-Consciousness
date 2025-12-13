from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class TemporalEchoParadox:

    def resolve(self, prev: np.ndarray, curr: np.ndarray, alpha: float=0.1) -> np.ndarray:
        return curr + alpha * (curr - prev)