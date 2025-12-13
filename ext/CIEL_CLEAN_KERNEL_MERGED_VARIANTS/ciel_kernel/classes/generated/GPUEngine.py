from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class GPUEngine:
    """Automatyczny wybór backendu dla ciężkich operacji (laplace/grad)."""

    def __init__(self, enable_gpu: bool=True, enable_numba: bool=True):
        self._cupy = None
        self.enable_numba = enable_numba
        if enable_gpu:
            try:
                import cupy as cp
                self._cupy = cp
            except Exception:
                self._cupy = None
        self._numba_njit = None
        if enable_numba:
            try:
                from numba import njit
                self._numba_njit = njit
            except Exception:
                self._numba_njit = None
        self._laplacian_cpu = self._build_laplacian_cpu()

    def xp(self):
        """Zwraca moduł: cupy lub numpy."""
        return self._cupy if self._cupy is not None else np

    def to_xp(self, arr: np.ndarray):
        """Przeniesienie tablicy do backendu (no-op dla NumPy)."""
        if self._cupy is None:
            return arr
        return self._cupy.asarray(arr)

    def to_np(self, arr):
        """Przeniesienie tablicy na CPU (NumPy)."""
        if self._cupy is None:
            return arr
        return self._cupy.asnumpy(arr)

    def gradient2(self, field):
        """Szybki grad 2D z backendem; unika pętli w Pythonie."""
        xp = self.xp()
        gx = xp.zeros_like(field)
        gy = xp.zeros_like(field)
        gx[:, 1:-1] = 0.5 * (field[:, 2:] - field[:, :-2])
        gy[1:-1, :] = 0.5 * (field[2:, :] - field[:-2, :])
        return (gy, gx)

    def laplacian(self, field):
        """Wersja GPU/CPU; dla CPU używa numba-JIT jeśli dostępne."""
        if self._cupy is not None:
            xp = self._cupy
            out = xp.zeros_like(field)
            out[1:-1, 1:-1] = field[2:, 1:-1] + field[:-2, 1:-1] + field[1:-1, 2:] + field[1:-1, :-2] - 4.0 * field[1:-1, 1:-1]
            return out
        return self._laplacian_cpu(field)

    def _build_laplacian_cpu(self):

        def lap_cpu(a: np.ndarray) -> np.ndarray:
            out = np.zeros_like(a)
            out[1:-1, 1:-1] = a[2:, 1:-1] + a[:-2, 1:-1] + a[1:-1, 2:] + a[1:-1, :-2] - 4.0 * a[1:-1, 1:-1]
            return out
        if self._numba_njit is not None:
            return self._numba_njit(cache=True, fastmath=True)(lap_cpu)
        return lap_cpu