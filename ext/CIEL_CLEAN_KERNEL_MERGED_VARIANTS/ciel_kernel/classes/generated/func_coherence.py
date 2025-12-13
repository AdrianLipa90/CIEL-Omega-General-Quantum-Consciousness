from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

def coherence(psi: np.ndarray) -> float:
    gx = np.zeros_like(psi)
    gy = np.zeros_like(psi)
    gx[:, 1:-1] = psi[:, 2:] - psi[:, :-2]
    gy[1:-1, :] = psi[2:, :] - psi[:-2, :]
    E = np.mean(np.abs(gx) ** 2 + np.abs(gy) ** 2)
    return float(1.0 / (1.0 + E))