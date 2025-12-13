from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def schumann_harmonics(base: float=7.83, k: int=1) -> float:
    return base * k