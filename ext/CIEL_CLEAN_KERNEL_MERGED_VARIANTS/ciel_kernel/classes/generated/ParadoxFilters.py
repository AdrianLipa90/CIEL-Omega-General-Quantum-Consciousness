from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import numpy as np

class ParadoxFilters:

    @staticmethod
    def twin_identity(psi: np.ndarray) -> np.ndarray:
        """
        Symetria „bliźniacza” (real/imag) – miękkie uporządkowanie fazy.
        """
        conj = np.conjugate(psi)
        return 0.5 * (psi + conj) + 0.5j * (psi - conj)

    @staticmethod
    def echo(prev: np.ndarray, curr: np.ndarray, k: float=0.08) -> np.ndarray:
        """
        Echo różnicowe: curr' = curr + k*(curr - prev).
        Działa jak delikatny momentum/damping w dziedzinie przestrzennej.
        """
        return curr + k * (curr - prev)

    @staticmethod
    def boundary_collapse(psi: np.ndarray, tol: float=0.001) -> np.ndarray:
        """
        Warunek brzegowy: „ściska” brzegi siatki ku wartościom średnim,
        co zapobiega rozbieganiu koherencji na krawędziach.
        """
        out = psi.copy()
        mean_val = np.mean(psi)
        out[0, :] = (1 - tol) * out[0, :] + tol * mean_val
        out[-1, :] = (1 - tol) * out[-1, :] + tol * mean_val
        out[:, 0] = (1 - tol) * out[:, 0] + tol * mean_val
        out[:, -1] = (1 - tol) * out[:, -1] + tol * mean_val
        return out