from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

def build_runtime(backend_obj: Optional[Any]=None, grid: int=96) -> OmegaRuntime:
    backend = BackendAdapter(backend_obj, grid_size=grid)
    drift = OmegaDriftCorePlus(SchumannClock(), drift_gain=0.04, harmonic_sweep=(1, 3), jitter=0.003)
    rcde = RCDECalibratorPro(lam=0.22, dt=0.05, sigma=0.6)
    csf = CSF2Kernel(dt=0.05)
    return OmegaRuntime(backend, drift, rcde, csf)