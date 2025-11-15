"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

# batch19_csf_memory.py
# CIEL/Ω – Batch 19: CSF2 + Pamięć/Introspekcja + ParadoxStress + Glue do backendu
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List
import numpy as np, json, math

# ── CSF2: pola Ψ–Σ–Λ–Ω (lite) ──────────────────────────────────────────────
@dataclass
class CSF2State:
    psi: np.ndarray           # pole świadomości (complex)
    sigma: np.ndarray         # pole struktury (real)
    lam: np.ndarray           # intencja (complex)
    omega: np.ndarray         # świat/otoczenie (real)
    def clone(self)->"CSF2State":
        return CSF2State(self.psi.copy(), self.sigma.copy(), self.lam.copy(), self.omega.copy())

def _lap(a: np.ndarray)->np.ndarray:
    out=np.zeros_like(a); out[1:-1,1:-1]=(a[2:,1:-1]+a[:-2,1:-1]+a[1:-1,2:]+a[1:-1,:-2]-4.0*a[1:-1,1:-1]); return out

@dataclass
class CSF2Kernel:
    dt: float=0.05
    k_psi: float=0.8
    k_sigma: float=0.6
    k_couple: float=0.5
    k_world: float=0.2
    def step(self, s: CSF2State)->CSF2State:
        psi, sigma, lam, om = s.psi, s.sigma, s.lam, s.omega
        dpsi = 1j*self.k_psi*_lap(psi) + self.k_couple*(lam*sigma - om*psi)
        dsig = self.k_sigma*(np.abs(psi)**2 - sigma) - 0.1*sigma**2
        dome = 0.05*_lap(om) - 0.02*(om - np.mean(om))
        dlam = 0.1*(psi*np.conj(psi)) - 0.05*lam
        psi2 = psi + self.dt*dpsi
        sigma2 = np.clip(sigma + self.dt*dsig, 0.0, 2.0)
        omega2 = om + self.dt*dome
        lam2 = lam + self.dt*dlam
        # renorm
        n = float(np.sqrt(np.mean(np.abs(psi2)**2)) + 1e-12); psi2 = psi2/n
        return CSF2State(psi2, sigma2, lam2, omega2)

# ── Pamięć / Synchronizacja ────────────────────────────────────────────────
@dataclass
class MemorySynchronizer:
    alpha: float=0.92  # zapominanie
    beta: float=0.08   # ślad Ψ→Σ
    ms: Optional[np.ndarray]=None
    def update(self, sigma: np.ndarray, psi: np.ndarray)->np.ndarray:
        if self.ms is None: self.ms = sigma.copy()
        self.ms = self.alpha*self.ms + self.beta*np.abs(psi)
        return self.ms

@dataclass
class CSFReporter:
    def metrics(self, s: CSF2State)->Dict[str,float]:
        grad=np.gradient(s.psi)
        E = float(np.mean(np.abs(grad[0])**2 + np.abs(grad[1])**2))
        coh = float(1.0/(1.0+E))
        return {"coherence":coh,"sigma_mean": float(np.mean(s.sigma)), "omega_var": float(np.var(s.omega))}
    def to_json(self, s: CSF2State)->str:
        return json.dumps({"sigma_mean": float(np.mean(s.sigma)), "coh": self.metrics(s)["coherence"]}, ensure_ascii=False)

# ── Introspekcja: Dissociation (korelacja ego↔świat) ───────────────────────
@dataclass
class Introspection:
    low_thr: float=0.3; high_thr: float=0.8
    def state(self, ego: np.ndarray, world: np.ndarray)->Dict[str,Any]:
        a=ego.real.ravel(); b=world.real.ravel()
        a=(a-a.mean())/(a.std()+1e-12); b=(b-b.mean())/(b.std()+1e-12)
        rho=float(np.dot(a,b)/(len(a)-1))
        st="integration" if rho>self.high_thr else "dissociation" if rho<self.low_thr else "mixed"
        return {"rho":rho,"state":st}

# ── Paradoxy: kontrolowany stres semantyczny ───────────────────────────────
@dataclass
class ParadoxStress:
    strength: float=0.1
    def apply(self, s: CSF2State)->CSF2State:
        jitter = (np.random.rand(*s.psi.shape)-0.5)*self.strength
        s_new = s.clone()
        s_new.psi = s.psi*np.exp(1j*jitter)
        return s_new

# ── Glue do backendu: „cielFullQuantumCore” (interfejs wąski) ──────────────
@dataclass
class BackendGlue:
    """Adapter: CSF2 ↔ pełny backend (cielFullQuantumCore.py).
    Zakładamy, że backend ma metody:
      - set_fields(psi: np.ndarray, sigma: np.ndarray)
      - step(dt: float) -> None
      - get_fields() -> Tuple[np.ndarray, np.ndarray]
    """
    backend: Any
    def push(self, s: CSF2State)->None:
        self.backend.set_fields(s.psi, s.sigma)
    def pull(self, s: CSF2State)->CSF2State:
        psi,sigma = self.backend.get_fields()
        return CSF2State(psi, sigma, s.lam, s.omega)
    def evolve(self, s: CSF2State, steps:int=5, dt:float=0.02)->CSF2State:
        self.push(s)
        for _ in range(steps): self.backend.step(dt=dt)
        return self.pull(s)

# ── Szybki runner CSF2 (samodzielny) ───────────────────────────────────────
def make_csf2_seed(n:int=96)->CSF2State:
    x=np.linspace(-2,2,n); y=np.linspace(-2,2,n); X,Y=np.meshgrid(x,y)
    psi=np.exp(-(X**2+Y**2))*np.exp(1j*(X+0.2*Y))
    sigma=np.exp(-(X**2+Y**2)/2.0)
    lam=np.ones_like(psi)*0.1
    omega=np.zeros_like(sigma)
    # renorm
    psi=psi/(np.sqrt(np.mean(np.abs(psi)**2))+1e-12)
    return CSF2State(psi.astype(np.complex128), sigma.astype(np.float64), lam.astype(np.complex128), omega.astype(np.float64))

def csf2_demo(steps:int=20)->Dict[str,float]:
    st=make_csf2_seed(); ker=CSF2Kernel(); mem=MemorySynchronizer(); rep=CSFReporter(); stress=ParadoxStress(0.06)
    for k in range(steps):
        st=ker.step(st)
        if (k%5)==0: st=stress.apply(st)
        mem.update(st.sigma, st.psi)
    return rep.metrics(st)

if __name__=="__main__":
    print(csf2_demo(24))