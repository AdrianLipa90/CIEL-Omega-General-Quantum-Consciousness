# -*- coding: utf-8 -*-
"""
CIEL/0 – Batch5 Patch (no-FFT, only new pieces)
Dodaje WYŁĄCZNIE brakujące klocki:
- Lie4MatrixEngine: generatory LIE₄ + komutatory (wektoryzowane)
- SigmaSeries: dynamiczna ewolucja Σ(t) (bez FFT)
- ParadoxFilters: TwinIdentity, Echo, BoundaryCollapse (stabilizacja)
- VisualCore: lekkie mapowania amplitude/phase → tensor wizualny (bez rysowania)

Nie dubluje CSF/RCDE/Σ-statycznego/etyki/kolorów z poprzednich batchy.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import numpy as np

# ============================================================================
# 1) LIE₄: generatory i komutatory (macierze 4×4; baza Minkowskiego diag(+,-,-,-))
# ============================================================================
@dataclass
class Lie4MatrixEngine:
    """Minimalny silnik LIE₄ (SO(3,1) + translacje jako rozszerzenie formalne)."""
    # Metrika Minkowskiego η = diag(1, -1, -1, -1)
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
            raise ValueError("mu != nu required")
        s1 = self._E(mu, nu) * self.eta[nu, nu]
        s2 = self._E(nu, mu) * self.eta[mu, mu]
        return s1 - s2

    def basis_so31(self) -> Dict[Tuple[int,int], np.ndarray]:
        """Zwraca słownik generatorów { (μ,ν): M_{μν} } dla μ<ν."""
        gens = {}
        for mu in range(4):
            for nu in range(mu + 1, 4):
                gens[(mu, nu)] = self.lorentz_generator(mu, nu)
        return gens

    @staticmethod
    def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """[A,B] = AB − BA (wektoryzacja NumPy)."""
        return A @ B - B @ A

    def lie_bracket_table(self) -> Dict[Tuple[Tuple[int,int],Tuple[int,int]], np.ndarray]:
        """Tablica komutatorów dla bazy so(3,1)."""
        basis = self.basis_so31()
        keys = list(basis.keys())
        table = {}
        for i, k1 in enumerate(keys):
            for k2 in keys[i:]:
                C = self.commutator(basis[k1], basis[k2])
                table[(k1, k2)] = C
                table[(k2, k1)] = -C
        return table

# ============================================================================
# 2) SigmaSeries: dynamiczna ewolucja niezmiennika Σ(t) (bez FFT)
#    Σ_{t+1} = Σ_t + α^t (1 − Σ_t),   Σ_0 ∈ (0,1),  α∈(0,1]
# ============================================================================
@dataclass
class SigmaSeries:
    alpha: float = 0.618      # „złoty” współczynnik przyrostu
    sigma0: float = 0.42      # startowa koherencja
    steps: int = 256

    def run(self) -> np.ndarray:
        t = np.arange(self.steps, dtype=float)
        a_pow = self.alpha ** t                # [T]
        sigma = np.empty(self.steps, dtype=float)
        s = float(self.sigma0)
        for i in range(self.steps):
            s = s + a_pow[i] * (1.0 - s)
            sigma[i] = s
        return sigma

    def apply_to_field(self, field: np.ndarray) -> np.ndarray:
        """
        Zastosuj ostatnią wartość Σ_T jako delikatną normalizację amplitudy pola.
        Bez FFT: wyłącznie skalowanie, stabilne numerycznie.
        """
        sigma_T = float(self.run()[-1])
        amp = np.sqrt(np.mean(np.abs(field)**2)) + 1e-12
        target = np.sqrt(sigma_T)
        return field * (target / amp)

# ============================================================================
# 3) ParadoxFilters: z „Paradoksy_2” – filtry stabilizujące (no-FFT)
# ============================================================================
class ParadoxFilters:
    @staticmethod
    def twin_identity(psi: np.ndarray) -> np.ndarray:
        """
        Symetria „bliźniacza” (real/imag) – miękkie uporządkowanie fazy.
        """
        conj = np.conjugate(psi)
        # 0.5*(psi + conj) = Re(psi),  0.5j*(psi - conj) = i·Im(psi)  → zachowuje amplitudę
        return 0.5 * (psi + conj) + 0.5j * (psi - conj)

    @staticmethod
    def echo(prev: np.ndarray, curr: np.ndarray, k: float = 0.08) -> np.ndarray:
        """
        Echo różnicowe: curr' = curr + k*(curr - prev).
        Działa jak delikatny momentum/damping w dziedzinie przestrzennej.
        """
        return curr + k * (curr - prev)

    @staticmethod
    def boundary_collapse(psi: np.ndarray, tol: float = 1e-3) -> np.ndarray:
        """
        Warunek brzegowy: „ściska” brzegi siatki ku wartościom średnim,
        co zapobiega rozbieganiu koherencji na krawędziach.
        """
        out = psi.copy()
        mean_val = np.mean(psi)
        out[0, :]   = (1 - tol) * out[0, :]   + tol * mean_val
        out[-1, :]  = (1 - tol) * out[-1, :]  + tol * mean_val
        out[:, 0]   = (1 - tol) * out[:, 0]   + tol * mean_val
        out[:, -1]  = (1 - tol) * out[:, -1]  + tol * mean_val
        return out

# ============================================================================
# 4) VisualCore: lekkie mapowania amplitude/phase → „obraz” (bez wykresów)
#    Jeśli masz ColorMap z Batch4, możesz użyć mapowania kolorów RGB;
#    tutaj zwracamy neutralne tensory (amplitude, phase_sin, phase_cos).
# ============================================================================
@dataclass
class VisualCore:
    """
    Nie rysuje – tylko przygotowuje dane wizualne (H×W×C) do dalszego użycia.
    Kanały:
      0: amplitude (|ψ|)
      1: phase_sin (sin(arg ψ))
      2: phase_cos (cos(arg ψ))
    """
    clip_amp: Optional[float] = None  # np. 99-percentyl do przycięcia szumów

    def tensorize(self, psi: np.ndarray) -> np.ndarray:
        amp = np.abs(psi)
        if self.clip_amp is not None:
            hi = np.percentile(amp, self.clip_amp)
            amp = np.clip(amp, 0.0, hi) / (hi + 1e-12)
        else:
            amp = amp / (np.max(amp) + 1e-12)

        ph = np.angle(psi)
        ph_s = np.sin(ph)
        ph_c = np.cos(ph)
        # [H,W,3]
        return np.stack([amp, ph_s, ph_c], axis=-1)

# ============================================================================
# 5) Mini-test integracyjny (bez wizualizacji i bez FFT)
# ============================================================================
def _demo():
    # sztuczne pole
    n = 96
    x = np.linspace(-2, 2, n); y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X**2 + Y**2)) * np.exp(1j * (X + 0.5*Y))

    # 1) Lie₄ – pokaż rozmiar bazy i normę przykładowego komutatora
    L = Lie4MatrixEngine()
    basis = L.basis_so31()
    keys = sorted(basis.keys())
    C01_02 = L.commutator(basis[(0,1)], basis[(0,2)])
    lie_sig = float(np.linalg.norm(C01_02))

    # 2) SigmaSeries – zastosuj delikatną normalizację
    sigma = SigmaSeries(alpha=0.7, sigma0=0.4, steps=128)
    psi1 = sigma.apply_to_field(psi0)

    # 3) Filtry paradoksalne
    psi2 = ParadoxFilters.twin_identity(psi1)
    psi3 = ParadoxFilters.echo(prev=psi1, curr=psi2, k=0.1)
    psi4 = ParadoxFilters.boundary_collapse(psi3, tol=1e-3)

    # 4) VisualCore – przygotuj tensor wizualny (H×W×3)
    vis = VisualCore(clip_amp=99.0)
    T = vis.tensorize(psi4)

    print("LIE₄ basis size:", len(basis))
    print("‖[M01, M02]‖ =", f"{lie_sig:.4f}")
    print("SigmaSeries last Σ:", f"{sigma.run()[-1]:.4f}")
    print("Visual tensor shape:", T.shape)

if __name__ == "__main__":
    _demo()