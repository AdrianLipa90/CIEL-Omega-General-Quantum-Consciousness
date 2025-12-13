import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special, ndimage
from scipy.interpolate import RectBivariateSpline
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings
import numpy.typing as npt
from sympy import isprime

class Lie4Algebra:

    def __init__(self, constants: Lie4Constants):
        self.C = constants
        self.generators = self._initialize_generators()

    def _initialize_generators(self) -> Dict[str, np.ndarray]:
        gens = {}
        M = []
        indices = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        for i, j in indices:
            G = np.zeros((4, 4), dtype=np.complex128)
            G[i, j] = 1.0
            G[j, i] = -1.0
            M.append(G)
        gens['M'] = np.array(M)
        P = np.zeros((4, 4, 4), dtype=np.complex128)
        for mu in range(4):
            P[mu, mu, mu] = 1.0
        gens['P'] = P
        Q_base = np.array([[0.6, 0.3, 0.2, 0.1], [0.3, 0.7, 0.2, 0.1], [0.2, 0.3, 0.8, 0.1], [0.1, 0.2, 0.3, 0.9]], dtype=np.complex128)
        Q = []
        for mu in range(4):
            Q_mu = Q_base.copy()
            Q_mu[mu, mu] *= 1.5
            Q_mu = (Q_mu + Q_mu.T.conj()) / 2
            Q.append(Q_mu)
        gens['Q'] = np.array(Q)
        Omega = np.array([[1.0, 0.5j, -0.3, 0.2j], [-0.5j, 1.0, 0.4j, -0.1], [-0.3, -0.4j, 1.0, 0.3j], [-0.2j, -0.1, -0.3j, 1.0]], dtype=np.complex128)
        gens['Omega'] = Omega
        return gens

    def commutator(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        return A @ B - B @ A

    def structure_constants(self) -> np.ndarray:
        n = self.C.TOTAL_DIM
        f = np.zeros((n, n, n), dtype=np.complex128)
        gen_list = []
        for M_gen in self.generators['M']:
            gen_list.append(M_gen)
        for mu in range(4):
            gen_list.append(self.generators['P'][mu])
        for Q_gen in self.generators['Q']:
            gen_list.append(Q_gen)
        gen_list.append(self.generators['Omega'])
        for a in range(min(len(gen_list), n)):
            for b in range(min(len(gen_list), n)):
                comm = self.commutator(gen_list[a], gen_list[b])
                for c in range(min(len(gen_list), n)):
                    f[a, b, c] = np.trace(comm @ gen_list[c].T.conj())
        return f

    def adjoint_action(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        return self.commutator(X, Y)

    def casimir_operator(self) -> np.ndarray:
        gen_list = []
        for M_gen in self.generators['M']:
            gen_list.append(M_gen)
        for mu in range(4):
            gen_list.append(self.generators['P'][mu])
        casimir = np.zeros((4, 4), dtype=np.complex128)
        for gen in gen_list:
            casimir += gen @ gen
        return casimir