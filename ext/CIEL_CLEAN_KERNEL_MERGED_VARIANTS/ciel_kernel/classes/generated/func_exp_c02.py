from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def exp_c02() -> Dict[str, Any]:
    """Dryf fazowy w czasie – lekkie oscylacje."""
    psi, _, _ = make_seed()
    for t in range(20):
        psi *= np.exp(1j * 0.05 * t)
        psi = psi + 1j * 0.01 * laplacian2(psi)
        psi /= field_norm(psi)
    return {'norm': field_norm(psi), 'coherence': coherence_metric(psi)}