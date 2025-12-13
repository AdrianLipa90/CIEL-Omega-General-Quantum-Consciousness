from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

class SchumannClock:
    base_hz: float = 7.83
    start_t: float = field(default_factory=time.perf_counter)

    def phase(self, t: Optional[float]=None, k: int=1) -> float:
        """Faza w [0, 2π) dla harmonicznej k."""
        t_now = time.perf_counter() - self.start_t if t is None else t
        omega = 2.0 * math.pi * schumann_harmonics(self.base_hz, k)
        return omega * t_now % (2.0 * math.pi)

    def carrier(self, shape: Tuple[int, int], amp: float=1.0, k: int=1) -> np.ndarray:
        """Fala nośna (skalująca) do modulacji pola."""
        ph = self.phase(k=k)
        return amp * np.exp(1j * ph) * np.ones(shape, dtype=np.complex128)