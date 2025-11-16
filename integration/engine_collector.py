from __future__ import annotations

from typing import Any, Callable, Dict

from ciel.engine import CielEngine
from .runtime_orchestrator import RuntimeOrchestrator


def build_runtime_orchestrator(
    engine: CielEngine,
    sink: Callable[[Dict[str, Any]], None],
) -> RuntimeOrchestrator:
    """Build a RuntimeOrchestrator that sources input from ``CielEngine``.

    The collector is intentionally simple and deterministic: it invokes
    ``engine.step`` with a placeholder text to produce a single snapshot of the
    engine's processing pipeline. In future revisions this hook can be wired to
    real-time inputs without altering the orchestrator surface.
    """

    def collector() -> Dict[str, Any]:
        return engine.step("[integration-snapshot]")

    return RuntimeOrchestrator(collector=collector, sink=sink)
