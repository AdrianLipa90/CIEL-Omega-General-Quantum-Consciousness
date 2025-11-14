"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Compile glyph interpretations into executable instructions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class GlyphCompiler:
    def compile(self, glyphs: Iterable[str]) -> str:
        return "\n".join(glyphs)


__all__ = ["GlyphCompiler"]
