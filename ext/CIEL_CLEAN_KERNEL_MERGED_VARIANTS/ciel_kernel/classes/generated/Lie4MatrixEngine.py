from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import numpy as np

class Lie4MatrixEngine:
    """Minimalny silnik LIE₄ (SO(3,1) + translacje jako rozszerzenie formalne)."""
    eta: np.ndarray = field(default_factory=lambda: np.diag([1.0, -1.0, -1.0, -1.0]))

    def _E(self, i: int, j: int) -> np.ndarray:
        """Macierz z 1 na (i,j)."""
        M = np.zeros((4, 4), dtype=float)
        M[i, j] = 1.0
        return M

    def lorentz_generator(self, mu: int, nu: int) -> np.ndarray:
        """
        M_{μν} = E_{μν}·η_{νν} − E_{νμ}·η_{μμ},  (μ<ν)
        Generatory antysymetryczne względem metryki.
        """
        if mu == nu:
            raise ValueError('mu != nu required')
        s1 = self._E(mu, nu) * self.eta[nu, nu]
        s2 = self._E(nu, mu) * self.eta[mu, mu]
        return s1 - s2

    def basis_so31(self) -> Dict[Tuple[int, int], np.ndarray]:
        """Zwraca słownik generatorów { (μ,ν): M_{μν} } dla μ<ν."""
        gens = {}
        for mu in range(4):
            for nu in range(mu + 1, 4):
                gens[mu, nu] = self.lorentz_generator(mu, nu)
        return gens

    @staticmethod
    def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """[A,B] = AB − BA (wektoryzacja NumPy)."""
        return A @ B - B @ A

    def lie_bracket_table(self) -> Dict[Tuple[Tuple[int, int], Tuple[int, int]], np.ndarray]:
        """Tablica komutatorów dla bazy so(3,1)."""
        basis = self.basis_so31()
        keys = list(basis.keys())
        table = {}
        for i, k1 in enumerate(keys):
            for k2 in keys[i:]:
                C = self.commutator(basis[k1], basis[k2])
                table[k1, k2] = C
                table[k2, k1] = -C
        return table