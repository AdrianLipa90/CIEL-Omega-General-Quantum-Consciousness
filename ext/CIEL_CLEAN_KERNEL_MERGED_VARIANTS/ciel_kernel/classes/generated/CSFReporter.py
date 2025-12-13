from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List
import numpy as np, json, math

class CSFReporter:

    def metrics(self, s: CSF2State) -> Dict[str, float]:
        grad = np.gradient(s.psi)
        E = float(np.mean(np.abs(grad[0]) ** 2 + np.abs(grad[1]) ** 2))
        coh = float(1.0 / (1.0 + E))
        return {'coherence': coh, 'sigma_mean': float(np.mean(s.sigma)), 'omega_var': float(np.var(s.omega))}

    def to_json(self, s: CSF2State) -> str:
        return json.dumps({'sigma_mean': float(np.mean(s.sigma)), 'coh': self.metrics(s)['coherence']}, ensure_ascii=False)