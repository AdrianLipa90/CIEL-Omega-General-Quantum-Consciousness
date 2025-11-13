"""Compile glyph interpretations into executable instructions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class GlyphCompiler:
    def compile(self, glyphs: Iterable[str]) -> str:
        return "\n".join(glyphs)


__all__ = ["GlyphCompiler"]
