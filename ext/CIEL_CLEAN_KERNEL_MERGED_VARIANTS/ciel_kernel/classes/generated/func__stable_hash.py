from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

def _stable_hash(text: str) -> int:
    return int(hashlib.blake2b(text.encode('utf-8'), digest_size=8).hexdigest(), 16)