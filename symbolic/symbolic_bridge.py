"""Bridge connecting glyph pipelines with downstream consumers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .glyph_compiler import GlyphCompiler
from .glyph_pipeline import GlyphPipeline


@dataclass(slots=True)
class SymbolicBridge:
    pipeline: GlyphPipeline
    compiler: GlyphCompiler = field(default_factory=GlyphCompiler)

    def execute(self) -> str:
        glyphs = self.pipeline.run()
        return self.compiler.compile(glyphs)


__all__ = ["SymbolicBridge"]
