import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings

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
        gens['Q'] = np.array([np.diag(row) for row in Q_base])
        gens['I'] = np.array([(1.0 + 0.5j) * np.eye(4, dtype=np.complex128)])
        return gens