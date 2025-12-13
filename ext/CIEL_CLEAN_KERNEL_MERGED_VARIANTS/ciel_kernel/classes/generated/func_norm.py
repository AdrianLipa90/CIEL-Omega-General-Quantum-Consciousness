from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

def norm(psi: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12)