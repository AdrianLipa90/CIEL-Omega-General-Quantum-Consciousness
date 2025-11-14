"""High level helper describing an intention field.

The class provides a very small API that is sufficient for all existing import
sites.  It exposes deterministic behaviour that can be validated in tests while
remaining computationally cheap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

import numpy as np


@dataclass(slots=True)
class IntentionField:
    """Represent a normalised intention vector used across the code base."""

    channels: int = 12
    seed: int | None = None
    _history: List[np.ndarray] = field(default_factory=list, init=False, repr=False)

    def generate(self) -> np.ndarray:
        """Generate a deterministic vector using the configured seed."""

        rng = np.random.default_rng(self.seed)
        vector = rng.normal(size=self.channels)
        norm = np.linalg.norm(vector) or 1.0
        vector = vector / norm
        self._history.append(vector)
        return vector

    def project(self, values: Iterable[float]) -> float:
        """Project *values* on the last generated intention vector."""

        if not self._history:
            self.generate()
        vec = self._history[-1]
        arr = np.fromiter(values, dtype=float, count=len(vec))
        arr = arr[: vec.size]
        if arr.size < vec.size:
            arr = np.pad(arr, (0, vec.size - arr.size))
        return float(np.dot(vec, arr))

    def reset(self) -> None:
        """Forget the generated history."""

        self._history.clear()


__all__ = ["IntentionField"]
