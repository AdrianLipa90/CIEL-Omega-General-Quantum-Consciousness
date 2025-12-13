from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

def _normalize_profile(d: Dict[str, float]) -> Dict[str, float]:
    clipped = {k: max(0.0, float(v)) for k, v in d.items()}
    s = sum(clipped.values())
    if s <= 1e-12:
        return {k: 0.0 for k in clipped}
    return {k: v / s for k, v in clipped.items()}