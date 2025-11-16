from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Optional, TYPE_CHECKING


class LoopType(Enum):
    LC = auto()
    LO = auto()
    LB = auto()
    LP = auto()
    LI = auto()
    LS = auto()
    LM = auto()


@dataclass
class Loop:
    loop_id: str
    loop_type: LoopType
    contradiction: float
    phase: float
    glyph: "Glyph"
    ritual: Optional["Ritual"]
    curvature: float
    delta_memory: Any = None
    closed: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)


if TYPE_CHECKING:  # pragma: no cover
    from .glyphs import Glyph, Ritual
