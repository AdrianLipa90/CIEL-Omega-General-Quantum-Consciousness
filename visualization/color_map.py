"""Generate perceptually friendly colour maps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(slots=True)
class ColorMap:
    name: str = "aurora"

    def sample(self, n: int = 256) -> np.ndarray:
        x = np.linspace(0, 1, n)
        return np.stack([x, np.sqrt(x), x ** 0.3], axis=1)


__all__ = ["ColorMap"]
