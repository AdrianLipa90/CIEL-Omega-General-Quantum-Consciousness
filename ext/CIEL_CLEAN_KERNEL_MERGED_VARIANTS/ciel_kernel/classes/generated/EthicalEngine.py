from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

class EthicalEngine:
    """Dynamiczna ocena etyczna w oparciu o spójność, intencję i masę."""
    bound: float = 0.9
    history: list = field(default_factory=list)

    def evaluate(self, coherence: float, intention: float, mass: float) -> float:
        """Zwraca wartość etyczną (0–1)."""
        score = coherence * intention / (mass + 1e-12)
        value = np.tanh(score / self.bound)
        self.history.append(float(value))
        return float(value)

    def mean_score(self) -> float:
        return float(np.mean(self.history)) if self.history else 0.0