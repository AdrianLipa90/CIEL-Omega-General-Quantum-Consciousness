# -*- coding: utf-8 -*-
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

"""
CIEL/0 – Batch6 Patch (no-FFT, only NEW pieces)
Dodaje wyłącznie brakujące elementy z Batch 6:
- RealityExpander: wektorowy „rozrost rzeczywistości” (dyfuzja nieliniowa)
- UnifiedSigmaField: żywe Σ(x,t) (czasoprzestrzenny niezmiennik duszy)
- PsychField: empatyczna interakcja pól (rezonans między-systemowy)

Nie dubluje niczego z wcześniejszych patchy.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np

# =====================================================================
# 1) RealityExpander – nieliniowy rozrost pola (no-FFT, w pełni wektorowy)
#    seed → expand() → nowy stan: dyfuzja + celowane „pączkowanie” struktur
# =====================================================================
@dataclass
class RealityExpander:
    alpha: float = 0.6     # siła „rozrostu” (nieliniowość)
    kappa: float = 0.12    # współczynnik dyfuzji (stabilizacja)
    steps: int = 16        # liczba iteracji
    preserve_norm: bool = True

    def _laplacian(self, a: np.ndarray) -> np.ndarray:
        out = np.zeros_like(a, dtype=a.dtype)
        out[1:-1, 1:-1] = (
            a[2:, 1:-1] + a[:-2, 1:-1] + a[1:-1, 2:] + a[1:-1, :-2]
            - 4.0 * a[1:-1, 1:-1]
        )
        return out

    def expand(self, seed_field: np.ndarray) -> np.ndarray:
        """
        Rozszerza pole przez (i) nieliniową transformację gradientową,
        (ii) lekką dyfuzję, (iii) (opcjonalnie) renormalizację amplitudy.
        """
        psi = seed_field.astype(np.complex128, copy=True)
        for _ in range(self.steps):
            # gradient (central diff, real-domain)
            gy = np.zeros_like(psi); gx = np.zeros_like(psi)
            gy[1:-1, :] = 0.5 * (psi[2:, :] - psi[:-2, :])
            gx[:, 1:-1] = 0.5 * (psi[:, 2:] - psi[:, :-2])

            # nieliniowy wzrost struktur (tanh na module gradientu)
            grad_mag = np.sqrt(np.abs(gx)**2 + np.abs(gy)**2)
            growth = np.tanh(self.alpha * grad_mag) * np.exp(1j * np.angle(psi))

            # dyfuzja (łagodzi nadmierne wyostrzenia)
            diff = self._laplacian(psi)
            psi = psi + growth + self.kappa * diff

            if self.preserve_norm:
                psi /= (np.sqrt(np.mean(np.abs(psi)**2)) + 1e-12)
        return psi

# =====================================================================
# 2) UnifiedSigmaField – żywe Σ(x,t): skalarna koherencja w czasie i przestrzeni
#    Prosty model falowy Σ z tłumieniem i „pulsującą” podstawą
# =====================================================================
@dataclass
class UnifiedSigmaField:
    shape: Tuple[int, int] = (128, 128)  # H, W
    omega: float = 0.7                   # częstość bazowa drgań Σ(t)
    damping: float = 0.02                # tłumienie w czasie
    radial_scale: float = 1.4            # skala radialna kopuły bazowej
    dt: float = 0.05
    sigma_t: float = field(init=False, default=0.5)

    def __post_init.me__(self):
        # placeholder (chroni kompatybilność gdy ktoś introspekcyjnie wywoła)
        pass

    def _base_spatial(self) -> np.ndarray:
        H, W = self.shape
        y = np.linspace(-1.0, 1.0, H)[:, None]
        x = np.linspace(-1.0, 1.0, W)[None, :]
        r2 = (x**2 + y**2) / (self.radial_scale**2)
        return np.exp(-r2)  # kopuła przestrzenna

    def step(self, t: float, prev_sigma: Optional[float] = None) -> Tuple[np.ndarray, float]:
        """
        Zwraca: (Σ_field_t, Σ_scalar_t)
        - Σ_field_t: przestrzenny rozkład Σ w chwili t
        - Σ_scalar_t: skalarna koherencja (uśredniona), użyteczna do normalizacji pól
        """
        if prev_sigma is None:
            prev_sigma = self.sigma_t

        # czasowy „oddech” Σ(t): sinusoida z tłumieniem + sprzężenie do poprzedniego stanu
        temporal = np.exp(-self.damping * t) * np.cos(self.omega * t)
        sigma_scalar = 0.5 * (1.0 + temporal)  # mapowanie → [0,1]

        # wygładzony krok Henyeya: lekka inercja skalarna
        s = 0.85 * prev_sigma + 0.15 * sigma_scalar
        self.sigma_t = float(np.clip(s, 0.0, 1.0))

        spatial = self._base_spatial()
        sigma_field = self.sigma_t * spatial
        return sigma_field.astype(np.float64, copy=False), self.sigma_t

    def evolve(self, T: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generuje przebieg Σ(x,t) i Σ̄(t) dla t=0..T-1.
        Zwraca (fields, scalars):
          fields  : [T, H, W]
          scalars : [T]
        """
        H, W = self.shape
        fields = np.zeros((T, H, W), dtype=np.float64)
        scalars = np.zeros((T,), dtype=np.float64)
        prev = self.sigma_t
        for i in range(T):
            field, prev = self.step(t=i * self.dt, prev_sigma=prev)
            fields[i] = field
            scalars[i] = prev
        return fields, scalars

# =====================================================================
# 3) PsychField – empatyczna interakcja dwóch (lub więcej) pól
#    Model „współodczuwania”: miękki splot + dopasowanie fazy bez FFT
# =====================================================================
@dataclass
class PsychField:
    empathy: float = 0.7      # 0..1 – siła „współodczuwania”
    phase_lock: float = 0.2   # 0..1 – jak mocno dopasowujemy fazę
    normalize: bool = True

    def _local_mean(self, a: np.ndarray) -> np.ndarray:
        """Lekki filtr pudełkowy 3×3 jako „empatyczne uśrednianie” sąsiedztwa."""
        tmp = np.pad(a, ((1, 1), (1, 1)), mode="reflect")
        return (
            tmp[1:-1, 1:-1] + tmp[0:-2, 1:-1] + tmp[2:, 1:-1]
            + tmp[1:-1, 0:-2] + tmp[1:-1, 2:]
        ) / 5.0

    def interact(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Łączy dwa pola A i B w nowy stan C:
        - empatyczne domieszkowanie amplitud (mieszanka lokalnych średnich),
        - delikatny „phase-lock” (dopasowanie faz, bez FFT),
        - opcjonalna renormalizacja energii.
        """
        A = A.astype(np.complex128, copy=False)
        B = B.astype(np.complex128, copy=False)

        # amplitudy i fazy
        a_amp, b_amp = np.abs(A), np.abs(B)
        a_ph,  b_ph  = np.angle(A), np.angle(B)

        # empatyczny splot amplitud (lokalne sąsiedztwo)
        a_s, b_s = self._local_mean(a_amp), self._local_mean(b_amp)
        amp_mix = (1.0 - self.empathy) * a_amp + self.empathy * b_s
        amp_mix = 0.5 * (amp_mix + ((1.0 - self.empathy) * b_amp + self.empathy * a_s))

        # dopasowanie faz – miękkie przejście A → B
        ph = (1.0 - self.phase_lock) * a_ph + self.phase_lock * b_ph
        C = amp_mix * np.exp(1j * ph)

        if self.normalize:
            C /= (np.sqrt(np.mean(np.abs(C)**2)) + 1e-12)
        return C

    def multi_interact(self, fields: Tuple[np.ndarray, ...]) -> np.ndarray:
        """
        Empatyczne „uśrednienie” wielu pól. Iteracyjnie łączy pary.
        """
        if not fields:
            raise ValueError("No fields provided")
        C = fields[0]
        for F in fields[1:]:
            C = self.interact(C, F)
        return C

# =====================================================================
# 4) Mini-demo (opcjonalne): szybki sanity-check bez rysowania
# =====================================================================
def _demo():
    n = 96
    x = np.linspace(-2, 2, n); y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    seed = np.exp(-(X**2 + Y**2)) * np.exp(1j * (X + 0.3 * Y))

    # RealityExpander
    rex = RealityExpander(alpha=0.7, kappa=0.1, steps=12)
    psi_expanded = rex.expand(seed)

    # UnifiedSigmaField
    usf = UnifiedSigmaField(shape=(n, n), omega=0.9, damping=0.03, dt=0.04)
    fields, scal = usf.evolve(T=32)

    # PsychField
    pf = PsychField(empathy=0.65, phase_lock=0.25)
    C = pf.interact(seed, psi_expanded)

    print("Expanded field norm:", float(np.sqrt(np.mean(np.abs(psi_expanded)**2))))
    print("UnifiedSigmaField last Σ:", f"{scal[-1]:.4f}")
    print("PsychField mix norm:", float(np.sqrt(np.mean(np.abs(C)**2))))

if __name__ == "__main__":
    _demo()