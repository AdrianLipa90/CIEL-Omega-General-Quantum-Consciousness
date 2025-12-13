from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

class ColatzLie4Engine:
    steps: int = 64

    def collatz_seq(self, n: int) -> List[int]:
        assert n > 0
        seq = [n]
        while n != 1 and len(seq) < self.steps:
            n = 3 * n + 1 if n % 2 else n // 2
            seq.append(n)
        return seq

    def _E(self, i: int, j: int) -> np.ndarray:
        M = np.zeros((4, 4), dtype=float)
        M[i, j] = 1.0
        return M

    def lorentz_gen(self, mu: int, nu: int) -> np.ndarray:
        eta = np.diag([1.0, -1.0, -1.0, -1.0])
        s1 = self._E(mu, nu) * eta[nu, nu]
        s2 = self._E(nu, mu) * eta[mu, mu]
        return s1 - s2

    def invariant(self, n: int) -> Dict[str, float]:
        seq = self.collatz_seq(n)
        G = np.eye(4)
        for k, val in enumerate(seq[:8]):
            i = val % 3 + 1
            A = self.lorentz_gen(0, i)
            G = G @ (np.eye(4) + (0.05 + 0.01 * k) * A)
        detG = float(np.linalg.det(G))
        trG = float(np.trace(G))
        spec = float(np.max(np.real(np.linalg.eigvals(G))))
        return {'det': detG, 'trace': trG, 'spec': spec, 'len': len(seq)}