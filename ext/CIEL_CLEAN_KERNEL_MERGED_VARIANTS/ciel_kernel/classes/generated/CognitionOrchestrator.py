from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class CognitionOrchestrator:
    percept: PerceptiveLayer
    cortex: IntuitiveCortex
    predictor: PredictiveCore
    decider: DecisionCore
    pre_step: Optional[Callable[[int, Dict[str, Any]], None]] = None
    post_step: Optional[Callable[[int, Dict[str, Any]], None]] = None
    _intuition_hist: List[float] = field(default_factory=list, init=False)
    _log: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def run_cycle(self, steps: int, psi_supplier: Callable[[int], np.ndarray], sigma_supplier: Callable[[int], np.ndarray], options_supplier: Callable[[int, float, float], Dict[str, Dict[str, float]]]) -> List[Dict[str, Any]]:
        """
        psi_supplier(t)   → pole Ψ (H×W) w kroku t
        sigma_supplier(t) → pole Σ (H×W) w kroku t
        options_supplier(t, intuition, prediction) → kandydaci decyzji
        Zwraca listę logów ze wszystkich kroków.
        """
        self._intuition_hist.clear()
        self._log.clear()
        for t in range(steps):
            ctx: Dict[str, Any] = {'t': t}
            if self.pre_step:
                self.pre_step(t, ctx)
            psi = psi_supplier(t)
            sigma = sigma_supplier(t)
            percept = self.percept.compute(psi, sigma)
            ctx['percept_mean'] = float(np.mean(percept))
            self.cortex.ingest(percept)
            intuition = self.cortex.intuition(percept)
            self.cortex.update_entropy(percept, k=0.05)
            self._intuition_hist.append(intuition)
            ctx['intuition'] = float(intuition)
            pred = self.predictor.predict(self._intuition_hist)
            ctx['prediction'] = float(pred)
            options = options_supplier(t, intuition, pred)
            choice, scores = self.decider.decide(options)
            ctx['decision'] = choice
            ctx['scores'] = scores
            if self.post_step:
                self.post_step(t, ctx)
            self._log.append(ctx)
        return list(self._log)