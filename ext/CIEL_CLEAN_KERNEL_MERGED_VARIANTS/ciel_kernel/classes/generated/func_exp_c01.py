from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def exp_c01() -> Dict[str, Any]:
    """Stabilność normy bez dryfu."""
    psi, _, _ = make_seed()
    for _ in range(20):
        psi = psi + 1j * 0.02 * laplacian2(psi)
        psi /= field_norm(psi)
    return {'norm': field_norm(psi), 'coherence': coherence_metric(psi)}