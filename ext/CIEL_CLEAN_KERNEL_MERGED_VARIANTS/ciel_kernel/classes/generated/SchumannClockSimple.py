from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

class SchumannClock:
    base_hz: float = 7.83
    start_t: float = field(default_factory=time.perf_counter)

    def phase(self, k: int=1, at: Optional[float]=None) -> float:
        t = time.perf_counter() - self.start_t if at is None else at
        return 2.0 * math.pi * self.base_hz * k * t % (2.0 * math.pi)