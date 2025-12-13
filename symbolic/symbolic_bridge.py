"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Bridge connecting glyph pipelines with downstream consumers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

from .glyph_compiler import GlyphCompiler
from .glyph_pipeline import GlyphPipeline


@dataclass(slots=True)
class SymbolicBridge:
    pipeline: GlyphPipeline
    compiler: GlyphCompiler = field(default_factory=GlyphCompiler)
    palette: Dict[str, Tuple[float, float, float]] = field(
        default_factory=lambda: {
            "SOUL_BLUE": (0.2, 0.4, 0.9),
            "INTENTION_GOLD": (0.95, 0.8, 0.2),
            "ETHICS_WHITE": (1.0, 1.0, 0.95),
            "WARNING_RED": (0.9, 0.2, 0.2),
            "BALANCE_GREEN": (0.3, 0.9, 0.5),
        }
    )

    def execute(self) -> str:
        glyphs = self.pipeline.run()
        return self.compiler.compile(glyphs)

    def glyph_color(self, coherence: float, sigma_scalar: float) -> Tuple[float, float, float]:
        val = float(np.clip(coherence * sigma_scalar, 0.0, 1.0))
        if val < 0.3:
            base = np.array(self.palette["WARNING_RED"], dtype=float)
        elif val < 0.7:
            base = np.array(self.palette["INTENTION_GOLD"], dtype=float)
        else:
            base = np.array(self.palette["ETHICS_WHITE"], dtype=float)
        out = base * val + (1.0 - val) * np.array(self.palette["SOUL_BLUE"], dtype=float)
        return (float(out[0]), float(out[1]), float(out[2]))


__all__ = ["SymbolicBridge"]
