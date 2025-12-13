from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class SoulInvariantOperator:
    """Spektralna miara Σ: prosta, wektoryzowana, stabilna numerycznie."""
    eps: float = 1e-12

    def compute_sigma_invariant(self, field: np.ndarray) -> float:
        F = np.fft.fft2(field)
        power = np.abs(F) ** 2
        h, w = field.shape
        ky = np.fft.fftfreq(h)
        kx = np.fft.fftfreq(w)
        k2 = ky[:, None] ** 2 + kx[None, :] ** 2
        sigma = float(np.mean(power * np.log1p(k2 + self.eps)))
        return sigma

    def rescale_to_ethics_bound(self, field: np.ndarray, bound: float=0.9) -> np.ndarray:
        amp = np.sqrt(np.mean(np.abs(field) ** 2)) + self.eps
        target = np.sqrt(bound)
        return field * (target / amp)