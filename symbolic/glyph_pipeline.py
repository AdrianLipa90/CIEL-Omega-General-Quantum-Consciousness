"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Pipeline combining loading and interpreting glyph data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from .glyph_loader import CVOSDatasetLoader
from .glyph_interpreter import GlyphNode, GlyphNodeInterpreter


@dataclass(slots=True)
class GlyphPipeline:
    loader: CVOSDatasetLoader
    interpreter: GlyphNodeInterpreter = field(default_factory=GlyphNodeInterpreter)

    def run(self) -> List[str]:
        return [self.interpreter.interpret(g) for g in self.loader.load()]

    def combine(
        self,
        nodes: List[GlyphNode],
        color_weights: Optional[List[float]] = None,
        sigma_field: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        if not nodes:
            return {"coherence": 0.0, "color_mix": 0.0, "summary": ""}

        weights = np.ones(len(nodes), dtype=float) if color_weights is None else np.asarray(color_weights, dtype=float)
        if weights.size != len(nodes):
            weights = np.ones(len(nodes), dtype=float)
        weights = weights / (float(np.sum(weights)) + 1e-12)

        text_summary = [f"{node.name} × {w:.2f}" for w, node in zip(weights, nodes)]
        coherence = float(np.mean(weights))
        sigma_mod = float(np.mean(sigma_field)) if sigma_field is not None else 1.0
        color_mix = float(min(1.0, coherence * sigma_mod))
        return {"coherence": coherence, "color_mix": color_mix, "summary": " | ".join(text_summary)}


__all__ = ["GlyphPipeline"]
