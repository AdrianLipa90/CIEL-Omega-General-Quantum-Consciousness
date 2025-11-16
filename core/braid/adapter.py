from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .loops import Loop, LoopType
from .runtime import BraidRuntime


@dataclass
class KernelAdapter:
    runtime: BraidRuntime

    def encode_prompt(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[float, float, str]:
        magnitude = 1.0
        phase_offset = 0.0
        domain = "generic"
        return magnitude, phase_offset, domain

    def submit_prompt(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Loop:
        magnitude, phase_offset, domain = self.encode_prompt(prompt, context)
        loop = self.runtime.submit_intention(
            magnitude=magnitude,
            phase_offset=phase_offset,
            domain=domain,
            loop_type=LoopType.LB,
        )
        return loop

    def step(self, max_loops: int = 4) -> Dict[str, Any]:
        results = self.runtime.step(max_loops=max_loops)
        coherence = self.runtime.memory.coherence()
        scar_residual = self.runtime.scars.residual_curvature()
        avg_contradiction = (
            sum(loop.contradiction for (loop, _) in results) / len(results)
            if results
            else 0.0
        )
        E_val = coherence - avg_contradiction

        return {
            "executed": [
                {
                    "loop_id": loop.loop_id,
                    "success": success,
                    "contradiction": loop.contradiction,
                    "curvature": loop.curvature,
                    "phase": loop.phase,
                    "glyph": loop.glyph.name,
                    "ritual": loop.ritual.name if loop.ritual else None,
                    "closed": loop.closed,
                    "post_C": loop.meta.get("post_C"),
                    "post_P": loop.meta.get("post_P"),
                    "post_E": loop.meta.get("post_E"),
                }
                for (loop, success) in results
            ],
            "coherence": coherence,
            "avg_contradiction": avg_contradiction,
            "E": E_val,
            "scar_residual": scar_residual,
            "scar_count": len(self.runtime.scars.scars),
        }
