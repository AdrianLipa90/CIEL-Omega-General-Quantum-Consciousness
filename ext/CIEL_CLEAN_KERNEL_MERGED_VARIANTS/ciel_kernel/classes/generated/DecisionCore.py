from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class DecisionCore:
    min_score: float = 0.15

    def decide(self, options: Dict[str, Dict[str, float]]) -> Tuple[Optional[str], Dict[str, float]]:
        """
        options = {
          "action_name": {"intent":0..1, "ethic":0..1, "confidence":0..1},
          ...
        }
        Zwraca (najlepsza_akcja_lub_None, słownik_score_ów).
        """
        scores = {}
        best_key, best_val = (None, -np.inf)
        for k, v in options.items():
            s = float(v.get('intent', 0.0) * v.get('ethic', 0.0) * v.get('confidence', 0.0))
            scores[k] = s
            if s > best_val:
                best_key, best_val = (k, s)
        if best_val < self.min_score:
            return (None, scores)
        return (best_key, scores)