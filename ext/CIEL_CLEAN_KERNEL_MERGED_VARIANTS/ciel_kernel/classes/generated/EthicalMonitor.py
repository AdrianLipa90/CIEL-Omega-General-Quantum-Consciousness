from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

class EthicalMonitor:
    """Łączy silnik, strażnika i kolory w prosty model obserwacyjny."""
    engine: EthicalEngine = field(default_factory=EthicalEngine)
    lite: EthicalCoreLite = field(default_factory=EthicalCoreLite)

    def evaluate_and_color(self, coherence: float, intention: float, mass: float) -> tuple[float, tuple[float, float, float]]:
        """Ocena i wizualizacja stanu etycznego."""
        value = self.engine.evaluate(coherence, intention, mass)
        ok = self.lite.check(coherence, value)
        color = ColorMap.map_value(value if ok else value * 0.5)
        return (value, color)