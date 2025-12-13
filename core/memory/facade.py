from __future__ import annotations

from typing import Any


def build_orchestrator() -> Any:
    try:
        from core.memory.orchestrator import UnifiedMemoryOrchestrator

        return UnifiedMemoryOrchestrator()
    except Exception:
        from ciel_memory.orchestrator import UnifiedMemoryOrchestrator

        return UnifiedMemoryOrchestrator()


__all__ = [
    "build_orchestrator",
]
