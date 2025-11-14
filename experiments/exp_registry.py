"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Minimal experiment registry used in tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Iterable


@dataclass(slots=True)
class ExpRegistry:
    experiments: Dict[str, Callable[[], Dict[str, Any]]] = field(default_factory=dict)

    def add(self, name: str, fn: Callable[[], Dict[str, Any]]) -> None:
        self.experiments[name] = fn

    def run(self, names: Iterable[str]) -> Dict[str, Dict[str, Any]]:
        return {name: self.experiments[name]() for name in names if name in self.experiments}


__all__ = ["ExpRegistry"]
