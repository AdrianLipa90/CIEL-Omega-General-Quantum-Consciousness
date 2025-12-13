from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

def _lexical_diversity(text: str) -> float:
    ws = [w for w in re.findall('[A-Za-zÀ-ž0-9]+', text.lower())]
    return len(set(ws)) / max(1, len(ws)) if ws else 0.0