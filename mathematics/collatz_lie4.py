"""Collatz-Lie4 bridge toy implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class CollatzLie4Engine:
    seed: int = 5

    def iterate(self, steps: int = 10) -> List[int]:
        value = self.seed
        seq = [value]
        for _ in range(max(steps, 0)):
            value = value // 2 if value % 2 == 0 else 3 * value + 1
            seq.append(value)
        return seq


__all__ = ["CollatzLie4Engine"]
