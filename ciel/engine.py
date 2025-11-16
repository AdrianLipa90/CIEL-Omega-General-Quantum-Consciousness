"""High-level orchestration facade for the CIEL stack.

The :class:`CielEngine` composes the curated components across configuration,
wave simulation, cognition, affective processing, and memory coordination.
Behaviour remains deterministic and compositional by delegating work to the
underlying modules and returning a structured diagnostic payload.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

import logging

from config.ciel_config import CielConfig
from config.simulation_config import IntentionField
from wave.fourier_kernel import SpectralWaveField12D
from core.memory.orchestrator import UnifiedMemoryOrchestrator
from cognition.orchestrator import CognitionOrchestrator
from emotion.affective_orchestrator import AffectiveOrchestrator

log = logging.getLogger("CIEL.Engine")


@dataclass(slots=True)
class CielEngine:
    """Compose the primary orchestrators into a single callable engine."""

    config: CielConfig = field(default_factory=CielConfig)
    intention: IntentionField = field(default_factory=IntentionField)
    kernel: SpectralWaveField12D = field(default_factory=SpectralWaveField12D)
    memory: UnifiedMemoryOrchestrator = field(default_factory=UnifiedMemoryOrchestrator)
    cognition: CognitionOrchestrator = field(default_factory=CognitionOrchestrator)
    affect: AffectiveOrchestrator = field(default_factory=AffectiveOrchestrator)

    def boot(self) -> None:
        """Initialise the engine (placeholder for future lifecycle hooks)."""

        log.info("Booting CIEL Engine")

    def shutdown(self) -> None:
        """Tear down the engine (placeholder for future lifecycle hooks)."""

        log.info("Shutting down CIEL Engine")

    def step(self, text: str, *, context: str = "dialogue") -> Dict[str, object]:
        """Run a single processing step over the provided text input."""

        cleaned = (text or "").strip()
        if not cleaned:
            return {"status": "empty"}

        intention_vector = self._intention_to_list(self.intention.generate())
        simulation = self._run_kernel(intention_vector)

        D = self.memory.capture(context=context, sense=cleaned)
        tmp_out = self.memory.run_tmp(D)
        memorised = self.memory.promote_if_bifurcated(D, tmp_out)

        cognition_out = self.cognition.evaluate(
            stimulus=intention_vector, goals=intention_vector
        )
        affect_out = self.affect.run(ego=intention_vector, other=intention_vector)

        return {
            "status": "ok",
            "intention_vector": intention_vector,
            "simulation": simulation,
            "tmp_outcome": tmp_out,
            "memorised": memorised,
            "cognition": cognition_out,
            "affect": affect_out,
        }

    def _intention_to_list(self, vec: Any) -> List[float]:
        if hasattr(vec, "tolist"):
            try:
                return [float(v) for v in vec.tolist()]
            except Exception:  # pragma: no cover - defensive fallback
                pass
        try:
            return [float(v) for v in vec]
        except Exception:  # pragma: no cover - final fallback
            return [float(vec)]

    def _run_kernel(self, intention_vector: List[float]) -> Any:
        run = getattr(self.kernel, "run", None)
        if callable(run):
            try:
                return run()
            except TypeError:
                try:
                    return run([intention_vector])
                except TypeError:
                    return run(intention_vector)
        synthesise = getattr(self.kernel, "synthesise", None)
        if callable(synthesise):
            field, time_axis = synthesise(intention_vector)
            return {"field": field, "time_axis": time_axis}
        return None


__all__ = ["CielEngine"]
