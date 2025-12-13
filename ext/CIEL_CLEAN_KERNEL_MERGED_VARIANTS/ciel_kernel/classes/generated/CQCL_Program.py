from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

class CQCL_Program:
    intent: str
    semantic_tree: Dict[str, Any]
    semantic_hash: int
    quantum_variables: Dict[str, float]
    input_data: Optional[float] = None
    computation_path: List[int] = field(default_factory=list)
    execution_trace: List[Dict[str, Any]] = field(default_factory=list)