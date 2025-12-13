from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def _demo():
    reg = make_lab_registry()
    results = reg.run(['VYCH_BOOT_RITUAL', 'rcde_calibrated', 'ResCxParKer_lite'])
    for k, v in results.items():
        print(f'[{k}] → { {kk: round(vv, 5) if isinstance(vv, float) else vv for kk, vv in v.items()}}')