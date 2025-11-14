"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Tiny backend adapter orchestrating capture of metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any


@dataclass(slots=True)
class BackendAdapter:
    collector: Callable[[], Dict[str, Any]]
    last_payload: Dict[str, Any] = field(default_factory=dict, init=False)

    def run(self) -> Dict[str, Any]:
        self.last_payload = self.collector()
        return self.last_payload


__all__ = ["BackendAdapter"]
