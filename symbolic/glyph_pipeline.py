"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Pipeline combining loading and interpreting glyph data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from .glyph_loader import CVOSDatasetLoader
from .glyph_interpreter import GlyphNodeInterpreter


@dataclass(slots=True)
class GlyphPipeline:
    loader: CVOSDatasetLoader
    interpreter: GlyphNodeInterpreter = field(default_factory=GlyphNodeInterpreter)

    def run(self) -> List[str]:
        return [self.interpreter.interpret(g) for g in self.loader.load()]


__all__ = ["GlyphPipeline"]
