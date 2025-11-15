"""Optional runtime facade that wires the Braid subsystem."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence

from core.braid import (
    BraidRuntime,
    KernelAdapter,
    make_default_runtime,
)

from .information_flow import InformationFlow
from .runtime_orchestrator import RuntimeOrchestrator


@dataclass(slots=True)
class BraidEnabledRuntime:
    """Integrate :class:`BraidRuntime` with the core orchestration pipeline."""

    base_runtime: RuntimeOrchestrator
    info_flow: InformationFlow
    braid_runtime: BraidRuntime
    braid_adapter: KernelAdapter

    @classmethod
    def with_defaults(
        cls,
        collector: Any,
        backend_adapter: Any,
        glue_sink: Any,
        info_flow: InformationFlow,
    ) -> "BraidEnabledRuntime":
        """Create a runtime that wires together the existing components."""

        _ = backend_adapter  # maintained for API symmetry; base runtime handles adapters internally
        base_runtime = RuntimeOrchestrator(collector=collector, sink=glue_sink)
        braid_runtime = make_default_runtime()
        braid_adapter = KernelAdapter(runtime=braid_runtime)
        return cls(
            base_runtime=base_runtime,
            info_flow=info_flow,
            braid_runtime=braid_runtime,
            braid_adapter=braid_adapter,
        )

    def run_once(self, raw_input: Any) -> Dict[str, Any]:
        """Execute a single cycle through runtime, flow, and braid layers."""

        runtime_result = self._run_base_runtime(raw_input)
        signal = self._extract_signal(runtime_result, raw_input)
        flow_result = self.info_flow.step(signal)

        prompt = self._make_prompt_from_flow(flow_result)
        context = self._make_context_from_flow(flow_result)

        self.braid_adapter.submit_prompt(prompt, context=context)
        braid_result = self.braid_adapter.step(max_loops=4)

        return {
            "runtime": runtime_result,
            "flow": flow_result,
            "braid": braid_result,
        }

    def _run_base_runtime(self, raw_input: Any) -> Dict[str, Any]:
        try:
            return self.base_runtime.run_once(raw_input)
        except TypeError:
            return self.base_runtime.run_once()

    def _extract_signal(self, runtime_payload: Any, raw_input: Any) -> Iterable[float]:
        signal = None
        if isinstance(runtime_payload, dict):
            signal = runtime_payload.get("signal")
            if signal is None:
                signal = runtime_payload.get("samples")
        if signal is None:
            signal = raw_input
        if signal is None:
            return []
        if isinstance(signal, dict):
            signal = list(signal.values())
        if isinstance(signal, (list, tuple)):
            return [self._ensure_float(value) for value in signal]
        if isinstance(signal, Sequence):
            return [self._ensure_float(value) for value in list(signal)]
        if hasattr(signal, "__iter__"):
            return [self._ensure_float(value) for value in signal]
        return []

    def _ensure_float(self, value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _make_prompt_from_flow(self, flow_payload: Dict[str, Any]) -> str:
        emotion = flow_payload.get("emotion")
        soul_invariant = flow_payload.get("soul_invariant")
        summary_parts: List[str] = []
        if emotion is not None:
            summary_parts.append(f"emotion={emotion}")
        if soul_invariant is not None:
            summary_parts.append(f"soul_invariant={soul_invariant}")
        distribution = flow_payload.get("distribution")
        if distribution is not None:
            summary_parts.append(f"distribution={distribution}")
        if not summary_parts:
            summary_parts.append("no_flow_data")
        return " | ".join(summary_parts)

    def _make_context_from_flow(self, flow_payload: Dict[str, Any]) -> Dict[str, Any]:
        distribution = flow_payload.get("distribution")
        peak = 0.0
        if isinstance(distribution, Iterable):
            peak = max((self._ensure_float(value) for value in distribution), default=0.0)
        return {
            "emotion": flow_payload.get("emotion"),
            "soul_invariant": flow_payload.get("soul_invariant"),
            "distribution_peak": peak,
            "coherence": self.braid_runtime.memory.coherence(),
        }


__all__ = ["BraidEnabledRuntime"]
