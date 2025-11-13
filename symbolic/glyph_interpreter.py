"""Interpret glyphs into symbolic operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class GlyphNodeInterpreter:
    def interpret(self, glyph: dict[str, object]) -> str:
        name = glyph.get("name", "unknown")
        strokes = glyph.get("strokes", 0)
        return f"{name}:{strokes}"


__all__ = ["GlyphNodeInterpreter"]
