"""Parallel resonance simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any

import numpy as np

from evolution.omega_drift import OmegaDriftCore
from evolution.schumann_clock import SchumannClock
from mathematics.safe_operations import heisenberg_soft_clip_range


@dataclass(slots=True)
class ResonanceNode:
    name: str
    psi: np.ndarray
    sigma: float


@dataclass(slots=True)
class ResConnectParallel:
    nodes: List[ResonanceNode]
    drift_factory: callable = lambda: OmegaDriftCore(SchumannClock())
    history: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def step(self) -> None:
        drift = self.drift_factory()
        for node in self.nodes:
            node.psi = drift.step(node.psi, node.sigma)
            node.sigma = float(
                heisenberg_soft_clip_range(
                    np.mean(np.abs(node.psi) ** 2),
                    0.0,
                    1.2,
                )
            )
        if len(self.nodes) >= 2:
            base = self.nodes[0].psi
            empathy = [float(np.exp(-np.mean(np.abs(base - n.psi)))) for n in self.nodes[1:]]
            self.history.append({"empathy": float(np.mean(empathy))})


__all__ = ["ResConnectParallel", "ResonanceNode"]
