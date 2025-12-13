from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

class EthicalCoreLite:
    """Minimalny strażnik etyki – szybka kontrola spójności."""
    ETHICAL_BOUND = 0.9
    HARMONIC_TOL = 0.05

    @staticmethod
    def check(coherence: float, resonance: float) -> bool:
        """Zwraca True, jeśli system zachowuje równowagę etyczną."""
        return coherence * resonance > EthicalCoreLite.ETHICAL_BOUND - EthicalCoreLite.HARMONIC_TOL