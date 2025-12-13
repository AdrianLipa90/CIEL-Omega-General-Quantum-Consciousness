from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

class EmotionCore:
    """
    Trzyma i aktualizuje wektor emocji.
    Zakładamy składowe w [0,1], miękko normalizowane.
    """
    state: Dict[str, float] = field(default_factory=lambda: {'joy': 0.4, 'calm': 0.5, 'awe': 0.25, 'sadness': 0.2, 'anger': 0.1, 'stress': 0.15})
    inertia: float = 0.85

    def _norm(self) -> None:
        v = np.array(list(self.state.values()), dtype=float)
        vmax = float(np.max(v)) + 1e-12
        v = v / vmax
        for k, val in zip(self.state.keys(), v):
            self.state[k] = float(np.clip(val, 0.0, 1.0))

    def update(self, affect: Dict[str, float]) -> Dict[str, float]:
        """
        Aktualizuje stan emocji na podstawie wektora 'affect' (np. z EEG).
        affect może zawierać podzbiór kluczy; reszta pozostaje bez zmian.
        """
        for k, v in affect.items():
            if k in self.state:
                self.state[k] = float(self.inertia * self.state[k] + (1 - self.inertia) * v)
        self._norm()
        return dict(self.state)

    def summary_scalar(self) -> float:
        """
        Skalar nastroju: (joy + calm + awe) - (sadness + anger + stress), zmapowany do [0,1].
        """
        pos = self.state.get('joy', 0) + self.state.get('calm', 0) + self.state.get('awe', 0)
        neg = self.state.get('sadness', 0) + self.state.get('anger', 0) + self.state.get('stress', 0)
        s = 0.5 * (1.0 + np.tanh(0.8 * (pos - neg)))
        return float(np.clip(s, 0.0, 1.0))