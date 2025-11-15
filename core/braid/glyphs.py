from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .loops import Loop
    from .memory import BraidMemory


GlyphOp = Callable[["Loop", "BraidMemory"], None]
RitualOp = Callable[["Loop", "BraidMemory"], None]


@dataclass
class Glyph:
    name: str
    operator: GlyphOp
    domain: str = "generic"
    risk_level: str = "low"
    description: str = ""


@dataclass
class Ritual:
    name: str
    operator: RitualOp
    kind: str = "stabilizing"
    description: str = ""


@dataclass
class GlyphEngine:
    glyphs: Dict[str, Glyph] = field(default_factory=dict)

    def register(self, glyph: Glyph) -> None:
        self.glyphs[glyph.name] = glyph

    def get(self, name: str) -> Glyph:
        return self.glyphs[name]

    def choose_for(self, contradiction: float, domain: str = "generic") -> Glyph:
        candidates = [glyph for glyph in self.glyphs.values() if glyph.domain == domain]
        if not candidates:
            candidates = list(self.glyphs.values())
        risk_order = {"low": 0, "medium": 1, "high": 2}
        candidates.sort(key=lambda glyph: risk_order.get(glyph.risk_level, 1))
        return candidates[0]


@dataclass
class RitualEngine:
    rituals: Dict[str, Ritual] = field(default_factory=dict)

    def register(self, ritual: Ritual) -> None:
        self.rituals[ritual.name] = ritual

    def get(self, name: str) -> Ritual:
        return self.rituals[name]

    def choose_for(self, contradiction: float) -> Optional[Ritual]:
        candidates = [ritual for ritual in self.rituals.values() if ritual.kind == "stabilizing"]
        return candidates[0] if candidates else None
