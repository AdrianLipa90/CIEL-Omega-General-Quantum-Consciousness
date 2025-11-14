"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Back-end glue combining capture, analysis and persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any


@dataclass(slots=True)
class BackendGlue:
    callback: Callable[[Dict[str, Any]], None]
    history: list[Dict[str, Any]] = field(default_factory=list, init=False)

    def emit(self, payload: Dict[str, Any]) -> None:
        self.history.append(payload)
        self.callback(payload)


__all__ = ["BackendGlue"]
