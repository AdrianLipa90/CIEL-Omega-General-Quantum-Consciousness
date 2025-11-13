"""Minimal visualisation core for tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class VisualCore:
    path: Path

    def render(self, field: Iterable[Iterable[float]]) -> None:
        arr = np.array(list(map(list, field)))
        intensity = arr.mean()
        self.path.write_text(f"intensity={intensity:.6f}", encoding="utf-8")


__all__ = ["VisualCore"]
