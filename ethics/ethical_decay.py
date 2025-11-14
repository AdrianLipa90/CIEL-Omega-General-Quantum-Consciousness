"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Utility describing an exponential decay of ethical certainty.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EthicalDecay:
    rate: float = 0.1

    def apply(self, value: float, steps: int = 1) -> float:
        return float(value * (1.0 - self.rate) ** max(steps, 0))


__all__ = ["EthicalDecay"]
