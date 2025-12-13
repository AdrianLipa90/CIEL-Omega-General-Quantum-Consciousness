from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

class EmpathicEngine:
    """
    Miara empatii: E = exp(- mean(|A - B|)),  0..1
    Dodatkowo funkcja phase_blend do łagodnego zgrywania faz (opcjonalnie).
    """
    phase_lock: float = 0.2

    def resonate(self, field_a: np.ndarray, field_b: np.ndarray) -> float:
        A = np.asarray(field_a)
        B = np.asarray(field_b)
        diff = np.mean(np.abs(A - B))
        return float(np.exp(-diff))

    def phase_blend(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        A = A.astype(np.complex128, copy=False)
        B = B.astype(np.complex128, copy=False)
        a_ph = np.angle(A)
        b_ph = np.angle(B)
        ph = (1.0 - self.phase_lock) * a_ph + self.phase_lock * b_ph
        amp = 0.5 * (np.abs(A) + np.abs(B))
        C = amp * np.exp(1j * ph)
        C /= np.sqrt(np.mean(np.abs(C) ** 2)) + 1e-12
        return C