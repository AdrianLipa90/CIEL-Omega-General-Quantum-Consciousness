from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List
import numpy as np, json, math

class BackendGlue:
    """Adapter: CSF2 ↔ pełny backend (cielFullQuantumCore.py).
    Zakładamy, że backend ma metody:
      - set_fields(psi: np.ndarray, sigma: np.ndarray)
      - step(dt: float) -> None
      - get_fields() -> Tuple[np.ndarray, np.ndarray]
    """
    backend: Any

    def push(self, s: CSF2State) -> None:
        self.backend.set_fields(s.psi, s.sigma)

    def pull(self, s: CSF2State) -> CSF2State:
        psi, sigma = self.backend.get_fields()
        return CSF2State(psi, sigma, s.lam, s.omega)

    def evolve(self, s: CSF2State, steps: int=5, dt: float=0.02) -> CSF2State:
        self.push(s)
        for _ in range(steps):
            self.backend.step(dt=dt)
        return self.pull(s)