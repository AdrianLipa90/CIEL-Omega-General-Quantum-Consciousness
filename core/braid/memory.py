from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List
import cmath


@dataclass
class MemoryUnit:
    """Pojedynczy węzeł pamięci w polu warkoczowym."""

    content: Any
    phase: float
    weight: float = 1.0
    status: str = "open"

    def phasor(self) -> complex:
        """Zwraca μ_i e^{iΦ_i}."""

        return self.weight * cmath.exp(1j * self.phase)


@dataclass
class BraidMemory:
    """Pole pamięciowe M = {M_i, Φ_i, μ_i, status_i}."""

    units: List[MemoryUnit] = field(default_factory=list)

    def coherence(self) -> float:
        """C(t) = |Σ μ_i e^{iΦ_i}|."""

        if not self.units:
            return 0.0
        s = sum((u.phasor() for u in self.units), 0 + 0j)
        return abs(s)

    def add(
        self,
        content: Any,
        phase: float,
        weight: float = 1.0,
        status: str = "open",
    ) -> MemoryUnit:
        u = MemoryUnit(content=content, phase=phase, weight=weight, status=status)
        self.units.append(u)
        return u

    def mean_phasor(self) -> complex:
        """Średni phasor ważony wagami μ_i."""

        if not self.units:
            return 0 + 0j
        total_weight = sum(u.weight for u in self.units)
        if total_weight == 0:
            return 0 + 0j
        s = sum((u.phasor() for u in self.units), 0 + 0j)
        return s / total_weight
