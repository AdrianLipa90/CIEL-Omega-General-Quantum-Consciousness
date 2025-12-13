from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

def run_demo(steps: int=20, backend_obj: Optional[Any]=None) -> Dict[str, float]:
    rt = build_runtime(backend_obj, grid=96)
    st = make_seed(96)
    last_metrics = {}
    for _ in range(steps):
        st, last_metrics = rt.step(st, backend_steps=3, backend_dt=0.02)
    return last_metrics