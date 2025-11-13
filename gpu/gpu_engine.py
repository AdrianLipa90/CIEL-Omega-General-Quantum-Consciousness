"""Simple GPU helper that mirrors the original extension API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(slots=True)
class GPUEngine:
    enable_gpu: bool = True
    enable_numba: bool = True

    def __post_init__(self) -> None:
        self._cupy: Any | None = None
        if self.enable_gpu:
            try:  # pragma: no cover - optional dependency
                import cupy as cp  # type: ignore

                self._cupy = cp
            except Exception:
                self._cupy = None

    def xp(self):
        return self._cupy if self._cupy is not None else np

    def to_numpy(self, array):
        if self._cupy is None:
            return array
        return self._cupy.asnumpy(array)


__all__ = ["GPUEngine"]
