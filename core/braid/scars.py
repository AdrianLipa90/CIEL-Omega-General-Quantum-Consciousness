from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
import time
import uuid


@dataclass
class Scar:
    id: str
    contradiction: float
    glyph_name: str
    delta_memory_summary: str
    curvature: float
    phase: float
    scar_type: str
    resolved: bool = False
    timestamp: float = field(default_factory=time.time)


@dataclass
class ScarRegistry:
    scars: List[Scar] = field(default_factory=list)
    scar_budget: float = 1.0

    def residual_curvature(self) -> float:
        """Suma krzywizn nierozwiązanych blizn."""

        return sum(s.curvature for s in self.scars if not s.resolved)

    def can_execute(self, curvature: float) -> bool:
        """Sprawdza, czy nowa pętla zmieści się w budżecie κ."""

        return self.residual_curvature() + curvature <= self.scar_budget

    def register_scar(
        self,
        contradiction: float,
        glyph_name: str,
        curvature: float,
        phase: float,
        scar_type: str,
        delta_memory_summary: str = "",
    ) -> Scar:
        scar = Scar(
            id=str(uuid.uuid4()),
            contradiction=contradiction,
            glyph_name=glyph_name,
            delta_memory_summary=delta_memory_summary,
            curvature=curvature,
            phase=phase,
            scar_type=scar_type,
        )
        self.scars.append(scar)
        return scar

    def resolve_scar(self, scar_id: str) -> None:
        """Oznacz bliznę jako rozładowaną/zaszytą."""

        for scar in self.scars:
            if scar.id == scar_id:
                scar.resolved = True
                break
