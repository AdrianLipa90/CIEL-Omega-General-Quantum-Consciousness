from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

def _empathy(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.exp(-np.mean(np.abs(A - B))))