from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

def _sentiment(text: str) -> float:
    t = text.lower()
    p = sum((t.count(w) for w in _POS))
    n = sum((t.count(w) for w in _NEG))
    tot = p + n
    return p / tot if tot else 0.5