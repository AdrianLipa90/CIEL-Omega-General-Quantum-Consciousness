"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Runtime orchestrator tying together adapter and glue.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any

from .backend_adapter import BackendAdapter
from .backend_glue import BackendGlue


@dataclass(slots=True)
class RuntimeOrchestrator:
    collector: Callable[[], Dict[str, Any]]
    sink: Callable[[Dict[str, Any]], None]

    def run_once(self) -> Dict[str, Any]:
        adapter = BackendAdapter(self.collector)
        glue = BackendGlue(self.sink)
        payload = adapter.run()
        glue.emit(payload)
        return payload


__all__ = ["RuntimeOrchestrator"]
