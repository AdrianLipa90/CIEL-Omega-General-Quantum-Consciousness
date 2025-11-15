# -*- coding: utf-8 -*-
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

CIEL/Ω – Batch 17 (Experimental Lab: Ω-Drift + Schumann + RCDE + Micro-Tests)
Minimalny, samowystarczalny pakiet do uruchamiania 10 eksperymentów z Explore.zip.
Bez FFT. W pełni wektoryzowany. Gotowy do podpięcia pod wcześniejsze batch’e.

Zawiera:
- SchumannClock        → źródło odniesienia 7.83 Hz (i harmoniczne)
- OmegaDriftCore       → miękki dryf fazowy zsynchronizowany z zegarem Schumanna
- RCDECalibrator       → równowaga dynamiczna Σ↔Ψ (homeostat koherencji)
- ExpRegistry          → rejestr i runner eksperymentów z metrykami
- 10 eksperymentów (lite): c01, c02, a2ebdead, 47fdb331, 72b221d9,
                           rcde_calibrated, ResCxParKer(lite), VYCH_BOOT_RITUAL,
                           dissociation, noweparadoxy
Uwaga: „colatzsemAndLie4” dołączymy przy powrocie do „6 poprzednich”, jak prosiłeś.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

# ────────────────────────────────────────────────────────────────────────────
# 0) Pomocnicze metryki i narzędzia
# ────────────────────────────────────────────────────────────────────────────
def laplacian2(a: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a, dtype=a.dtype)
    out[1:-1, 1:-1] = (
        a[2:, 1:-1] + a[:-2, 1:-1] + a[1:-1, 2:] + a[1:-1, :-2] - 4.0 * a[1:-1, 1:-1]
    )
    return out

def field_norm(psi: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12)

def coherence_metric(psi: np.ndarray) -> float:
    gx = np.zeros_like(psi); gy = np.zeros_like(psi)
    gx[:, 1:-1] = psi[:, 2:] - psi[:, :-2]
    gy[1:-1, :] = psi[2:, :] - psi[:-2, :]
    E = np.mean(np.abs(gx) ** 2 + np.abs(gy) ** 2)
    return float(1.0 / (1.0 + E))  # im mniejsza energia gradientu, tym wyższa koherencja

def schumann_harmonics(base: float = 7.83, k: int = 1) -> float:
    return base * k

# ────────────────────────────────────────────────────────────────────────────
# 1) SchumannClock – źródło odniesienia rytmicznego (7.83 Hz)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class SchumannClock:
    base_hz: float = 7.83
    start_t: float = field(default_factory=time.perf_counter)

    def phase(self, t: Optional[float] = None, k: int = 1) -> float:
        """Faza w [0, 2π) dla harmonicznej k."""
        t_now = (time.perf_counter() - self.start_t) if t is None else t
        omega = 2.0 * math.pi * schumann_harmonics(self.base_hz, k)
        return (omega * t_now) % (2.0 * math.pi)

    def carrier(self, shape: Tuple[int, int], amp: float = 1.0, k: int = 1) -> np.ndarray:
        """Fala nośna (skalująca) do modulacji pola."""
        ph = self.phase(k=k)
        # Jednolite pole fazowe (lite) – wystarcza do testów:
        return amp * np.exp(1j * ph) * np.ones(shape, dtype=np.complex128)

# ────────────────────────────────────────────────────────────────────────────
# 2) OmegaDriftCore – zsynchronizowany dryf fazy (Σ-aware)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class OmegaDriftCore:
    clock: SchumannClock
    drift_gain: float = 0.05     # siła domieszki fazowej
    harmonic: int = 1            # która harmoniczna Schumanna
    renorm: bool = True

    def step(self, psi: np.ndarray, sigma_scalar: float = 1.0) -> np.ndarray:
        carrier = self.clock.carrier(psi.shape, amp=1.0, k=self.harmonic)
        # modulacja fazy skalowana przez Σ̄
        psi_next = psi * np.exp(1j * self.drift_gain * sigma_scalar) * carrier
        if self.renorm:
            psi_next /= field_norm(psi_next)
        return psi_next

# ────────────────────────────────────────────────────────────────────────────
# 3) RCDECalibrator – homeostat koherencji Σ↔Ψ (lite)
#    dΣ/dt = λ (‖Ψ‖² - Σ)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class RCDECalibrator:
    lam: float = 0.2
    dt: float = 0.05
    sigma: float = 0.5  # Σ̄ (skalar)

    def step(self, psi: np.ndarray) -> float:
        energy = field_norm(psi) ** 2
        self.sigma = float(self.sigma + self.dt * self.lam * (energy - self.sigma))
        self.sigma = float(np.clip(self.sigma, 0.0, 1.5))  # racjonalny zakres
        return self.sigma

# ────────────────────────────────────────────────────────────────────────────
# 4) Rejestr eksperymentów
# ────────────────────────────────────────────────────────────────────────────
ExpFn = Callable[[], Dict[str, Any]]

@dataclass
class ExpRegistry:
    exps: Dict[str, ExpFn] = field(default_factory=dict)

    def add(self, name: str, fn: ExpFn):
        self.exps[name] = fn

    def run(self, names: List[str]) -> Dict[str, Dict[str, Any]]:
        out = {}
        for n in names:
            if n in self.exps:
                out[n] = self.exps[n]()
        return out

# ────────────────────────────────────────────────────────────────────────────
# 5) Konfiguracja pola testowego (wspólna baza)
# ────────────────────────────────────────────────────────────────────────────
def make_seed(n: int = 96, a: float = 1.0, b: float = 0.3) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-2, 2, n); y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X**2 + Y**2)) * np.exp(1j * (a * X + b * Y))
    sigma0 = np.exp(-(X**2 + Y**2) / 2.0)
    return psi0.astype(np.complex128), sigma0.astype(np.float64), (X + 0j)

# ────────────────────────────────────────────────────────────────────────────
# 6) 10 eksperymentów (lite implementacje)
# ────────────────────────────────────────────────────────────────────────────
def exp_c01() -> Dict[str, Any]:
    """Stabilność normy bez dryfu."""
    psi, _, _ = make_seed()
    for _ in range(20):
        psi = psi + 1j * 0.02 * laplacian2(psi)
        psi /= field_norm(psi)
    return {"norm": field_norm(psi), "coherence": coherence_metric(psi)}

def exp_c02() -> Dict[str, Any]:
    """Dryf fazowy w czasie – lekkie oscylacje."""
    psi, _, _ = make_seed()
    for t in range(20):
        psi *= np.exp(1j * 0.05 * t)
        psi = psi + 1j * 0.01 * laplacian2(psi)
        psi /= field_norm(psi)
    return {"norm": field_norm(psi), "coherence": coherence_metric(psi)}

def exp_a2ebdead() -> Dict[str, Any]:
    """Synchronizacja dwóch pól – „śmierć” jako pełna zgoda fazowa."""
    A, _, _ = make_seed()
    B, _, _ = make_seed(b=0.6)
    for _ in range(30):
        A = A * np.conj(B)
        A /= field_norm(A); B /= field_norm(B)
        if np.mean(np.abs(A - B)) < 1e-3:
            return {"sync": True, "delta": float(np.mean(np.abs(A - B)))}
        # przeciwdziałaj trywialnemu wylądowaniu w zera:
        B = 0.5 * (B + A * np.exp(1j * 0.01))
    return {"sync": False, "delta": float(np.mean(np.abs(A - B)))}

def exp_47fdb331() -> Dict[str, Any]:
    """Generator harmonicznych Schumanna (metryki energii)."""
    clk = SchumannClock()
    n = 1024
    t = np.linspace(0, 1, n)
    omega = 2 * np.pi * schumann_harmonics(7.83, 1)
    sig = np.sin(omega * t) + 0.3 * np.sin(2 * omega * t)
    energy = float(np.mean(sig**2))
    return {"energy": energy, "rms": float(np.sqrt(energy))}

def exp_72b221d9() -> Dict[str, Any]:
    """Kontrolowany collapse fazy."""
    psi, _, _ = make_seed()
    for _ in range(25):
        ph = np.angle(psi)
        psi *= np.exp(-np.abs(ph) / 15.0)
        psi = psi + 1j * 0.005 * laplacian2(psi)
        psi /= field_norm(psi)
    return {"coherence": coherence_metric(psi), "norm": field_norm(psi)}

def exp_rcde_calibrated() -> Dict[str, Any]:
    """Homeostat Σ↔Ψ."""
    psi, _, _ = make_seed()
    rcde = RCDECalibrator(lam=0.25, dt=0.05, sigma=0.6)
    sigmas = []
    for _ in range(30):
        psi = psi + 1j * 0.01 * laplacian2(psi)
        psi /= field_norm(psi)
        sigmas.append(rcde.step(psi))
    return {"sigma_last": float(sigmas[-1]), "sigma_mean": float(np.mean(sigmas))}

def exp_rescxparker_lite() -> Dict[str, Any]:
    """Równoległa empatia (lite, sam proces – bez socketów)."""
    psiA, _, _ = make_seed(b=0.2)
    psiB, _, _ = make_seed(b=-0.2)
    clk = SchumannClock()
    drift = OmegaDriftCore(clk, drift_gain=0.03, harmonic=1)
    def empath(A, B):
        return float(np.exp(-np.mean(np.abs(A - B))))
    es = []
    for _ in range(20):
        psiA = drift.step(psiA, sigma_scalar=0.9)
        psiB = drift.step(psiB, sigma_scalar=0.9)
        es.append(empath(psiA, psiB))
    return {"empathy_mean": float(np.mean(es)), "empathy_last": float(es[-1])}

def exp_vych_boot_ritual() -> Dict[str, Any]:
    """Ceremonialny boot: align z 7.83 Hz i łagodna faza Ω."""
    psi, sigma, _ = make_seed()
    clk = SchumannClock()
    omega = OmegaDriftCore(clk, drift_gain=0.04, harmonic=1)
    rcde = RCDECalibrator(lam=0.2, dt=0.05, sigma=0.5)
    for _ in range(16):
        psi = omega.step(psi, sigma_scalar=rcde.sigma)
        rcde.step(psi)
    return {
        "boot_complete": True,
        "sigma": rcde.sigma,
        "coherence": coherence_metric(psi),
    }

def exp_dissociation() -> Dict[str, Any]:
    """Korelacja ego↔świat (dissociation vs integration)."""
    ego, _, _ = make_seed()
    world = np.roll(ego, 3, axis=0) * np.exp(1j * 0.2)
    a = ego.real.ravel(); b = world.real.ravel()
    a = (a - a.mean()) / (a.std() + 1e-12); b = (b - b.mean()) / (b.std() + 1e-12)
    rho = float(np.dot(a, b) / (len(a) - 1))
    state = "integration" if rho > 0.8 else ("dissociation" if rho < 0.3 else "mixed")
    return {"rho": rho, "state": state}

def exp_noweparadoxy() -> Dict[str, Any]:
    """Stres test sensu – kontrolowany chaos decyzji."""
    val = random.random()
    paradox = (1 - val) if random.random() > 0.5 else val
    # stabilizacja przez medianę z kilku losów
    vals = [random.random() for _ in range(9)]
    med = float(np.median(vals))
    return {"paradox_out": paradox, "median_noise": med}

# ────────────────────────────────────────────────────────────────────────────
# 7) Fabryka rejestru z 10 eksperymentami
# ────────────────────────────────────────────────────────────────────────────
def make_lab_registry() -> ExpRegistry:
    reg = ExpRegistry()
    reg.add("c01", exp_c01)
    reg.add("c02", exp_c02)
    reg.add("a2ebdead", exp_a2ebdead)
    reg.add("47fdb331", exp_47fdb331)
    reg.add("72b221d9", exp_72b221d9)
    reg.add("rcde_calibrated", exp_rcde_calibrated)
    reg.add("ResCxParKer_lite", exp_rescxparker_lite)
    reg.add("VYCH_BOOT_RITUAL", exp_vych_boot_ritual)
    reg.add("dissociation", exp_dissociation)
    reg.add("noweparadoxy", exp_noweparadoxy)
    return reg

# ────────────────────────────────────────────────────────────────────────────
# 8) Mini-runner (opcjonalny): szybki sanity test
# ────────────────────────────────────────────────────────────────────────────
def _demo():
    reg = make_lab_registry()
    results = reg.run(["VYCH_BOOT_RITUAL", "rcde_calibrated", "ResCxParKer_lite"])
    for k, v in results.items():
        print(f"[{k}] → { {kk: (round(vv,5) if isinstance(vv,float) else vv) for kk,vv in v.items()} }")

if __name__ == "__main__":
    _demo()