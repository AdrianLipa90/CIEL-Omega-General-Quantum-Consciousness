"""Utility describing an exponential decay of ethical certainty."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EthicalDecay:
    rate: float = 0.1

    def apply(self, value: float, steps: int = 1) -> float:
        return float(value * (1.0 - self.rate) ** max(steps, 0))


__all__ = ["EthicalDecay"]
