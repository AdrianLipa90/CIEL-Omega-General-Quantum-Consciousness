# -*- coding: utf-8 -*-
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

CIEL/Ω – Batch 18 (Drift & Memory Layer)
Nowe elementy (bez duplikatów względem Batch 17):
- OmegaDriftCorePlus    : rozszerzony dryf Schumanna (faza adapt., jitter, harmonic sweep)
- OmegaBootRitual       : rytuał startowy Ω (faza, kolor, intencja) – API
- RCDECalibratorPro     : homeostat Σ↔Ψ z adaptacją λ i celem Σ*
- ResConnectParallel    : lite wielowątkowy rezonans między-nodowy (bez socketów)
- DissociationAnalyzer  : korelacja ego↔świat + histereza reintegracji
- LongTermMemory        : trwała pamięć stanu (serializacja/delta-log)
- ColatzLie4Engine      : eksperymentalny most Collatz ↔ LIE₄ (inwarianty)

Wszystko no-FFT, wektorowo. Kompatybilne z: SchumannClock, RCDECalibrator (Batch 17).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

# ────────────────────────────────────────────────────────────────────────────
# 0) Wspólne narzędzia
# ────────────────────────────────────────────────────────────────────────────
def lap2(a: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a, dtype=a.dtype)
    out[1:-1, 1:-1] = (
        a[2:, 1:-1] + a[:-2, 1:-1] + a[1:-1, 2:] + a[1:-1, :-2] - 4.0 * a[1:-1, 1:-1]
    )
    return out

def norm(psi: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12)

def coherence(psi: np.ndarray) -> float:
    gx = np.zeros_like(psi); gy = np.zeros_like(psi)
    gx[:, 1:-1] = psi[:, 2:] - psi[:, :-2]
    gy[1:-1, :] = psi[2:, :] - psi[:-2, :]
    E = np.mean(np.abs(gx) ** 2 + np.abs(gy) ** 2)
    return float(1.0 / (1.0 + E))

@dataclass
class SchumannClock:
    base_hz: float = 7.83
    start_t: float = field(default_factory=time.perf_counter)
    def phase(self, k: int = 1, at: Optional[float] = None) -> float:
        t = (time.perf_counter() - self.start_t) if at is None else at
        return (2.0 * math.pi * self.base_hz * k * t) % (2.0 * math.pi)

# ────────────────────────────────────────────────────────────────────────────
# 1) OmegaDriftCorePlus – dryf z adaptacją fazy i „jitterem” (Schumann-aware)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class OmegaDriftCorePlus:
    clock: SchumannClock
    drift_gain: float = 0.045        # siła domieszki fazowej
    harmonic: int = 1                # bieżąca harmoniczna
    harmonic_sweep: Tuple[int, int] = (1, 3)  # zakres sweepu
    jitter: float = 0.004            # niewielki chaos fazy (stabilizacja rezonansu)
    renorm: bool = True

    def step(self, psi: np.ndarray, sigma_scalar: float = 1.0, t: Optional[float] = None) -> np.ndarray:
        # sweep harmoniczny zależny od Σ (im wyższa Σ, tym wyższa harmoniczna w granicach)
        hmin, hmax = self.harmonic_sweep
        h = int(np.clip(round(hmin + (hmax - hmin) * np.clip(sigma_scalar, 0.0, 1.0)), hmin, hmax))
        ph = self.clock.phase(k=h, at=t) + np.random.uniform(-self.jitter, self.jitter)
        psi_next = psi * np.exp(1j * (self.drift_gain * sigma_scalar + ph))
        if self.renorm:
            psi_next /= norm(psi_next)
        return psi_next

# ────────────────────────────────────────────────────────────────────────────
# 2) OmegaBootRitual – rytuał startowy Ω: faza, kolor, intencja (API)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class OmegaBootRitual:
    drift: OmegaDriftCorePlus
    steps: int = 16
    intent_bias: float = 0.12  # lekki skręt intencji (faza globalna)
    log: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def run(self, psi0: np.ndarray, sigma0: float = 0.5) -> Dict[str, Any]:
        psi = psi0.copy()
        sigma = float(sigma0)
        for i in range(self.steps):
            # miękki potencjał intencji (rotacja globalna)
            psi *= np.exp(1j * self.intent_bias)
            psi = self.drift.step(psi, sigma_scalar=sigma)
            # mikro-ewolucja pola (stabilizacja krawędzi)
            psi = psi + 1j * 0.01 * lap2(psi)
            psi /= norm(psi)
            # Σ – prosty oddech
            sigma = float(np.clip(0.92 * sigma + 0.08 * norm(psi) ** 2, 0.0, 1.2))
            self.log.append({"step": i, "sigma": sigma, "coh": coherence(psi)})
        return {"psi": psi, "sigma": sigma, "coherence": coherence(psi), "boot_complete": True}

# ────────────────────────────────────────────────────────────────────────────
# 3) RCDECalibratorPro – Σ↔Ψ z celem Σ* i adaptacją λ
#    dΣ/dt = λ(t) (Σ* − Σ),  Σ* ≈ ‖Ψ‖²  (można ustawić inaczej)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class RCDECalibratorPro:
    lam: float = 0.22
    dt: float = 0.05
    sigma: float = 0.5
    target_sigma_fn: Optional[Callable[[np.ndarray], float]] = None
    lam_bounds: Tuple[float, float] = (0.05, 0.5)

    def _target(self, psi: np.ndarray) -> float:
        if self.target_sigma_fn:
            return float(self.target_sigma_fn(psi))
        return float(norm(psi) ** 2)

    def step(self, psi: np.ndarray) -> float:
        target = self._target(psi)
        err = target - self.sigma
        # adaptacja λ: większy błąd → większa prędkość regulacji
        lam_adapt = float(np.clip(self.lam * (1 + 0.8 * abs(err)), *self.lam_bounds))
        self.sigma = float(self.sigma + self.dt * lam_adapt * err)
        self.sigma = float(np.clip(self.sigma, 0.0, 1.5))
        return self.sigma

# ────────────────────────────────────────────────────────────────────────────
# 4) ResConnectParallel – lite multi-node empathy (wątki, brak sieci)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class NodeState:
    name: str
    psi: np.ndarray
    sigma: float

def _empathy(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.exp(-np.mean(np.abs(A - B))))

@dataclass
class ResConnectParallel:
    nodes: List[NodeState]
    drift_factory: Callable[[], OmegaDriftCorePlus]
    max_workers: int = 4
    history: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def step(self):
        # Każdy node dryfuje osobno (wątki)
        threads = []
        results: Dict[str, Tuple[np.ndarray, float]] = {}
        lock = threading.Lock()

        def evolve(node: NodeState):
            drift = self.drift_factory()
            psi = drift.step(node.psi, sigma_scalar=node.sigma)
            # prosty ruch stabilizujący
            psi = psi + 1j * 0.01 * lap2(psi)
            psi /= norm(psi)
            sig = float(np.clip(0.9 * node.sigma + 0.1 * norm(psi) ** 2, 0.0, 1.2))
            with lock:
                results[node.name] = (psi, sig)

        # uruchom
        for n in self.nodes:
            th = threading.Thread(target=evolve, args=(n,), daemon=True)
            threads.append(th); th.start()
        for th in threads: th.join()

        # zaktualizuj
        for n in self.nodes:
            psi, sig = results[n.name]
            n.psi = psi; n.sigma = sig

        # empatia średnia
        if len(self.nodes) >= 2:
            ems = []
            base = self.nodes[0].psi
            for n in self.nodes[1:]:
                ems.append(_empathy(base, n.psi))
            self.history.append({"empathy_mean": float(np.mean(ems)), "nodes": len(self.nodes)})

    def snapshot(self) -> Dict[str, Any]:
        return {
            "nodes": [{"name": n.name, "sigma": n.sigma, "coh": coherence(n.psi)} for n in self.nodes],
            "last_empathy": (self.history[-1]["empathy_mean"] if self.history else None)
        }

# ────────────────────────────────────────────────────────────────────────────
# 5) DissociationAnalyzer – korelacja ego↔świat z histerezą reintegracji
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class DissociationAnalyzer:
    low_thr: float = 0.3
    high_thr: float = 0.8
    hysteresis: float = 0.05
    state: str = field(default="mixed", init=False)

    def step(self, ego: np.ndarray, world: np.ndarray) -> Dict[str, Any]:
        a = ego.real.ravel(); b = world.real.ravel()
        a = (a - a.mean()) / (a.std() + 1e-12); b = (b - b.mean()) / (b.std() + 1e-12)
        rho = float(np.dot(a, b) / (len(a) - 1))

        # histereza: progi „wejścia” i „wyjścia” stanu
        if self.state != "dissociation" and rho < (self.low_thr - self.hysteresis):
            self.state = "dissociation"
        elif self.state != "integration" and rho > (self.high_thr + self.hysteresis):
            self.state = "integration"
        elif self.state not in ("dissociation", "integration"):
            self.state = "mixed"

        # propozycja reintegracji: miękka domieszka fazy świata do ego
        blend = None
        if self.state == "dissociation":
            phase = np.angle(world)
            blend = ego * (0.9) + 0.1 * np.exp(1j * phase)
            blend /= norm(blend)

        return {"rho": rho, "state": self.state, "reintegration_suggestion": blend}

# ────────────────────────────────────────────────────────────────────────────
# 6) LongTermMemory – trwała pamięć stanów (serialize/restore + delta-log)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class LongTermMemory:
    """Lekka pamięć epizodyczna – nic nie zapisuje na dysk, ale potrafi serializować."""
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def put(self, label: str, psi: np.ndarray, sigma: float, meta: Optional[Dict[str, Any]] = None):
        payload = {
            "label": label,
            "sigma": float(sigma),
            "shape": psi.shape,
            "psi_real": psi.real.astype(np.float32).tolist(),
            "psi_imag": psi.imag.astype(np.float32).tolist(),
            "meta": meta or {}
        }
        payload["hash"] = hashlib.sha256(json.dumps(payload["psi_real"][:64]).encode()).hexdigest()[:16]
        self.entries.append(payload)

    def export_json(self) -> str:
        return json.dumps(self.entries, ensure_ascii=False)

    def load_json(self, data: str):
        self.entries = json.loads(data)

    def restore(self, idx: int = -1) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        e = self.entries[idx]
        re = np.array(e["psi_real"], dtype=np.float32).reshape(e["shape"])
        im = np.array(e["psi_imag"], dtype=np.float32).reshape(e["shape"])
        psi = (re + 1j * im).astype(np.complex128)
        return psi, float(e["sigma"]), e.get("meta", {})

# ────────────────────────────────────────────────────────────────────────────
# 7) ColatzLie4Engine – most Collatz ↔ LIE₄ (inwarianty eksperymentalne)
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class ColatzLie4Engine:
    steps: int = 64

    def collatz_seq(self, n: int) -> List[int]:
        assert n > 0
        seq = [n]
        while n != 1 and len(seq) < self.steps:
            n = (3*n + 1) if (n % 2) else (n // 2)
            seq.append(n)
        return seq

    def _E(self, i: int, j: int) -> np.ndarray:
        M = np.zeros((4, 4), dtype=float); M[i, j] = 1.0; return M

    def lorentz_gen(self, mu: int, nu: int) -> np.ndarray:
        eta = np.diag([1.0, -1.0, -1.0, -1.0])
        s1 = self._E(mu, nu) * eta[nu, nu]; s2 = self._E(nu, mu) * eta[mu, mu]
        return s1 - s2

    def invariant(self, n: int) -> Dict[str, float]:
        seq = self.collatz_seq(n)
        # budujemy produkt losowej kombinacji generatorów według sekwencji
        G = np.eye(4)
        for k, val in enumerate(seq[:8]):  # krótko, by zachować stabilność
            i = (val % 3) + 1  # 1..3
            A = self.lorentz_gen(0, i)
            G = G @ (np.eye(4) + (0.05 + 0.01*k) * A)
        detG = float(np.linalg.det(G))
        trG = float(np.trace(G))
        spec = float(np.max(np.real(np.linalg.eigvals(G))))
        # inwariant Collatz-LIE (eksperymentalny, bez interpretacji fizycznej)
        return {"det": detG, "trace": trG, "spec": spec, "len": len(seq)}

# ────────────────────────────────────────────────────────────────────────────
# 8) Mini-demo (opcjonalne): sanity check tej warstwy
# ────────────────────────────────────────────────────────────────────────────
def _demo():
    # pole startowe
    n = 96
    x = np.linspace(-2, 2, n); y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X**2 + Y**2)) * np.exp(1j * (X + 0.2*Y))

    # DRIFT + BOOT
    clk = SchumannClock()
    drift = OmegaDriftCorePlus(clk, drift_gain=0.04, harmonic_sweep=(1, 3), jitter=0.003)
    boot = OmegaBootRitual(drift, steps=12, intent_bias=0.1)
    out = boot.run(psi0, sigma0=0.55)
    print("Ω Boot:", {"sigma": round(out["sigma"], 4), "coh": round(out["coherence"], 4)})

    # RCDE Pro
    rcde = RCDECalibratorPro(lam=0.22, dt=0.05, sigma=0.6)
    for _ in range(10):
        out["psi"] = out["psi"] + 1j * 0.01 * lap2(out["psi"]); out["psi"] /= norm(out["psi"])
        rcde.step(out["psi"])
    print("RCDE Pro Σ:", round(rcde.sigma, 4))

    # ResConnectParallel – 3 nody
    nodes = [
        NodeState("A", psi0.copy(), 0.5),
        NodeState("B", psi0*np.exp(1j*0.3), 0.6),
        NodeState("C", psi0*np.exp(1j*0.6), 0.55),
    ]
    net = ResConnectParallel(nodes, drift_factory=lambda: OmegaDriftCorePlus(clk))
    for _ in range(5): net.step()
    print("ResConnect snapshot:", net.snapshot())

    # DissociationAnalyzer
    da = DissociationAnalyzer()
    ego = psi0; world = np.roll(psi0, 4, axis=1) * np.exp(1j*0.25)
    diss = da.step(ego, world)
    print("Dissociation:", {"rho": round(diss["rho"], 4), "state": diss["state"]})

    # LongTermMemory
    ltm = LongTermMemory()
    ltm.put("post-boot", out["psi"], sigma=out["sigma"], meta={"coh": out["coherence"]})
    js = ltm.export_json()
    psi_rest, sigma_rest, meta_rest = ltm.restore(-1)
    print("LTM:", {"len": len(ltm.entries), "sigma_rest": round(sigma_rest,4), "meta": meta_rest})

    # ColatzLie4Engine
    cl4 = ColatzLie4Engine(steps=64)
    inv = cl4.invariant(27)
    print("Collatz-LIE4 inv:", {k: (round(v,5) if isinstance(v,(int,float)) else v) for k,v in inv.items()})

if __name__ == "__main__":
    _demo()