from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

class DissociationAnalyzer:
    low_thr: float = 0.3
    high_thr: float = 0.8
    hysteresis: float = 0.05
    state: str = field(default='mixed', init=False)

    def step(self, ego: np.ndarray, world: np.ndarray) -> Dict[str, Any]:
        a = ego.real.ravel()
        b = world.real.ravel()
        a = (a - a.mean()) / (a.std() + 1e-12)
        b = (b - b.mean()) / (b.std() + 1e-12)
        rho = float(np.dot(a, b) / (len(a) - 1))
        if self.state != 'dissociation' and rho < self.low_thr - self.hysteresis:
            self.state = 'dissociation'
        elif self.state != 'integration' and rho > self.high_thr + self.hysteresis:
            self.state = 'integration'
        elif self.state not in ('dissociation', 'integration'):
            self.state = 'mixed'
        blend = None
        if self.state == 'dissociation':
            phase = np.angle(world)
            blend = ego * 0.9 + 0.1 * np.exp(1j * phase)
            blend /= norm(blend)
        return {'rho': rho, 'state': self.state, 'reintegration_suggestion': blend}