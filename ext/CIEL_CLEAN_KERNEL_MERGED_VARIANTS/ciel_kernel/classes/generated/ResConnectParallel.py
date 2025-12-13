from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

class ResConnectParallel:
    nodes: List[NodeState]
    drift_factory: Callable[[], OmegaDriftCorePlus]
    max_workers: int = 4
    history: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def step(self):
        threads = []
        results: Dict[str, Tuple[np.ndarray, float]] = {}
        lock = threading.Lock()

        def evolve(node: NodeState):
            drift = self.drift_factory()
            psi = drift.step(node.psi, sigma_scalar=node.sigma)
            psi = psi + 1j * 0.01 * lap2(psi)
            psi /= norm(psi)
            sig = float(np.clip(0.9 * node.sigma + 0.1 * norm(psi) ** 2, 0.0, 1.2))
            with lock:
                results[node.name] = (psi, sig)
        for n in self.nodes:
            th = threading.Thread(target=evolve, args=(n,), daemon=True)
            threads.append(th)
            th.start()
        for th in threads:
            th.join()
        for n in self.nodes:
            psi, sig = results[n.name]
            n.psi = psi
            n.sigma = sig
        if len(self.nodes) >= 2:
            ems = []
            base = self.nodes[0].psi
            for n in self.nodes[1:]:
                ems.append(_empathy(base, n.psi))
            self.history.append({'empathy_mean': float(np.mean(ems)), 'nodes': len(self.nodes)})

    def snapshot(self) -> Dict[str, Any]:
        return {'nodes': [{'name': n.name, 'sigma': n.sigma, 'coh': coherence(n.psi)} for n in self.nodes], 'last_empathy': self.history[-1]['empathy_mean'] if self.history else None}