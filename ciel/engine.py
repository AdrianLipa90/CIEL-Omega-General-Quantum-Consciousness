"""High-level orchestration facade for the CIEL stack.

The :class:`CielEngine` glues together the curated components exposed across
configuration, wave simulation, cognition, affective processing, and memory
coordination.  The class keeps behaviour deterministic and compositional by
delegating all heavy lifting to the underlying modules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Sequence

import numpy as np

from cognition.orchestrator import CognitionOrchestrator
from config.ciel_config import CielConfig
from config.simulation_config import IntentionField
from emotion.affective_orchestrator import AffectiveOrchestrator
from wave.fourier_kernel import SpectralWaveField12D

try:
    from core.memory.orchestrator import UnifiedMemoryOrchestrator
except ImportError:  # pragma: no cover - repo profile uses vendor repo orchestrator
    from ciel_memory.orchestrator import UnifiedMemoryOrchestrator


def _as_list(values: Iterable[float]) -> list[float]:
    return [float(v) for v in values]


@dataclass(slots=True)
class CielEngine:
    """Compose the primary orchestrators into a single callable engine."""

    config: CielConfig = field(default_factory=CielConfig)
    intention: IntentionField = field(default_factory=lambda: IntentionField(seed=0))
    wave: SpectralWaveField12D = field(default_factory=SpectralWaveField12D)
    memory: UnifiedMemoryOrchestrator = field(default_factory=UnifiedMemoryOrchestrator)
    cognition: CognitionOrchestrator = field(default_factory=CognitionOrchestrator)
    affective: AffectiveOrchestrator = field(default_factory=AffectiveOrchestrator)

    def process(self, signal: Sequence[float] | None = None) -> Dict[str, Any]:
        """Run a full pipeline over the provided *signal* and return diagnostics."""

        field, time_axis = self.wave.synthesise(signal)
        intention_vector = self.intention.generate()
        cognition_out = self.cognition.evaluate(
            stimulus=intention_vector, goals=intention_vector
        )
        affective_out = self.affective.run(
            ego=intention_vector, other=intention_vector
        )

        memory_vector = self.memory.capture(
            context="ciel.engine",
            sense=self._safe_repr(signal),
            associations=None,
            meta={"novelty_hint": True},
        )
        tmp_out = self.memory.run_tmp(memory_vector)

        return {
            "config": self.config.as_dict(),
            "wave": {
                "time_axis": _as_list(time_axis),
                "field_shape": list(field.shape),
            },
            "intention": _as_list(intention_vector),
            "cognition": cognition_out,
            "affect": affective_out,
            "memory": {
                "tmp_out": tmp_out.get("OUT", {}),
                "report_count": len(self.memory._tmp_reports),
            },
        }

    def _safe_repr(self, payload: Sequence[float] | None) -> str:
        if payload is None:
            return "[]"
        arr = np.asarray(list(payload), dtype=float)
        return np.array2string(arr, separator=", ", precision=4)


__all__ = ["CielEngine"]
