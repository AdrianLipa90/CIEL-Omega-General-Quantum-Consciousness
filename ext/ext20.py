# batch20_backend_bridge.py
# CIEL/Ω – Batch 20: Backend Bridge & Runtime Orchestrator
# Spina: Batch17(Ω-Drift/RCDE) + Batch19(CSF2/Pamięć/Introspekcja) → backend (cielFullQuantumCore)
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

# ── Importy lekkie z Batch 17/18/19 (skopiowane minimalne wersje interfejsów) ─────────
# Jeśli masz pliki z poprzednich batchy jako moduły, możesz zamiast tego: from batch18_drift_memory import ...
def _lap(a: np.ndarray)->np.ndarray:
    out=np.zeros_like(a); out[1:-1,1:-1]=(a[2:,1:-1]+a[:-2,1:-1]+a[1:-1,2:]+a[1:-1,:-2]-4.0*a[1:-1,1:-1]); return out
def _norm(psi: np.ndarray)->float: return float(np.sqrt(np.mean(np.abs(psi)**2))+1e-12)
def _coh(psi: np.ndarray)->float:
    gx=np.zeros_like(psi); gy=np.zeros_like(psi)
    gx[:,1:-1]=psi[:,2:]-psi[:,:-2]; gy[1:-1,:]=psi[2:,:]-psi[:-2,:]
    E=np.mean(np.abs(gx)**2+np.abs(gy)**2); return float(1.0/(1.0+E))

@dataclass
class SchumannClock:
    base_hz: float = 7.83
    start_t: float = field(default_factory=time.perf_counter)
    def phase(self, k:int=1, at:Optional[float]=None)->float:
        t=(time.perf_counter()-self.start_t) if at is None else at
        return (2.0*math.pi*self.base_hz*k*t)%(2.0*math.pi)

@dataclass
class OmegaDriftCorePlus:
    clock: SchumannClock
    drift_gain: float=0.045
    harmonic_sweep: Tuple[int,int]=(1,3)
    jitter: float=0.004
    renorm: bool=True
    def step(self, psi: np.ndarray, sigma_scalar: float=1.0, t: Optional[float]=None)->np.ndarray:
        hmin,hmax=self.harmonic_sweep
        h=int(np.clip(round(hmin+(hmax-hmin)*np.clip(sigma_scalar,0,1)),hmin,hmax))
        ph=self.clock.phase(k=h,at=t)+np.random.uniform(-self.jitter,self.jitter)
        psi=psi*np.exp(1j*(self.drift_gain*sigma_scalar+ph))
        if self.renorm: psi/= _norm(psi)
        return psi

@dataclass
class RCDECalibratorPro:
    lam: float=0.22; dt: float=0.05; sigma: float=0.5
    lam_bounds: Tuple[float,float]=(0.05,0.5)
    def step(self, psi: np.ndarray)->float:
        target=float(_norm(psi)**2); err=target-self.sigma
        lam_adapt=float(np.clip(self.lam*(1+0.8*abs(err)), *self.lam_bounds))
        self.sigma=float(np.clip(self.sigma+self.dt*lam_adapt*err,0.0,1.5))
        return self.sigma

@dataclass
class CSF2State:
    psi: np.ndarray; sigma: np.ndarray; lam: np.ndarray; omega: np.ndarray
    def clone(self)->"CSF2State": return CSF2State(self.psi.copy(), self.sigma.copy(), self.lam.copy(), self.omega.copy())

@dataclass
class CSF2Kernel:
    dt: float=0.05; k_psi: float=0.8; k_sigma: float=0.6; k_couple: float=0.5; k_world: float=0.2
    def step(self, s: CSF2State)->CSF2State:
        dpsi = 1j*self.k_psi*_lap(s.psi) + self.k_couple*(s.lam*s.sigma - s.omega*s.psi)
        dsig = self.k_sigma*(np.abs(s.psi)**2 - s.sigma) - 0.1*s.sigma**2
        dome = 0.05*_lap(s.omega) - 0.02*(s.omega - np.mean(s.omega))
        dlam = 0.1*(s.psi*np.conj(s.psi)) - 0.05*s.lam
        psi2 = s.psi + self.dt*dpsi; psi2 = psi2/(_norm(psi2)+1e-12)
        sigma2 = np.clip(s.sigma + self.dt*dsig, 0.0, 2.0)
        omega2 = s.omega + self.dt*dome
        lam2 = s.lam + self.dt*dlam
        return CSF2State(psi2, sigma2, lam2, omega2)

@dataclass
class MemorySynchronizer:
    alpha: float=0.92; beta: float=0.08
    ms: Optional[np.ndarray]=None
    def update(self, sigma: np.ndarray, psi: np.ndarray)->np.ndarray:
        if self.ms is None: self.ms = sigma.copy()
        self.ms = self.alpha*self.ms + self.beta*np.abs(psi)
        return self.ms

@dataclass
class Introspection:
    low_thr: float=0.3; high_thr: float=0.8
    def state(self, ego: np.ndarray, world: np.ndarray)->Dict[str,float|str]:
        a=ego.real.ravel(); b=world.real.ravel()
        a=(a-a.mean())/(a.std()+1e-12); b=(b-b.mean())/(b.std()+1e-12)
        rho=float(np.dot(a,b)/(len(a)-1))
        st="integration" if rho>self.high_thr else "dissociation" if rho<self.low_thr else "mixed"
        return {"rho": rho, "state": st}

# ── Backend Adapter ─────────────────────────────────────────────────────────
class BackendAdapter:
    """
    Oczekuje backendu z metodami:
      - set_fields(psi: np.ndarray, sigma: np.ndarray)
      - step(dt: float) -> None
      - get_fields() -> Tuple[np.ndarray, np.ndarray]
    Jeśli ich nie ma – działa tryb awaryjny (wewnętrzny CSF2Kernel).
    """
    def __init__(self, backend: Optional[Any]=None, grid_size: int=96):
        self._fallback_kernel = CSF2Kernel(dt=0.02)
        self._fallback_state: Optional[Tuple[np.ndarray,np.ndarray]] = None
        self.backend = backend
        self.grid_size = grid_size

        if self.backend is None:
            # przy starcie tworzymy stan awaryjny
            x=np.linspace(-2,2,grid_size); y=np.linspace(-2,2,grid_size)
            X,Y=np.meshgrid(x,y)
            psi=np.exp(-(X**2+Y**2))*np.exp(1j*(X+0.2*Y)); psi/=(_norm(psi)+1e-12)
            sigma=np.exp(-(X**2+Y**2)/2.0)
            self._fallback_state = (psi.astype(np.complex128), sigma.astype(np.float64))

    def set_fields(self, psi: np.ndarray, sigma: np.ndarray)->None:
        if self.backend is not None and hasattr(self.backend, "set_fields"):
            self.backend.set_fields(psi, sigma)
        else:
            self._fallback_state = (psi.copy(), sigma.copy())

    def step(self, dt: float)->None:
        if self.backend is not None and hasattr(self.backend, "step"):
            self.backend.step(dt=dt)
        else:
            # prosta ewolucja fallback (tylko na psi, sigma) – lam/omega pomijamy
            if self._fallback_state is None: return
            psi, sigma = self._fallback_state
            s = CSF2State(psi, sigma, np.ones_like(psi)*0.1, np.zeros_like(sigma))
            self._fallback_kernel.dt = dt
            s2 = self._fallback_kernel.step(s)
            self._fallback_state = (s2.psi, s2.sigma)

    def get_fields(self)->Tuple[np.ndarray,np.ndarray]:
        if self.backend is not None and hasattr(self.backend, "get_fields"):
            return self.backend.get_fields()
        else:
            assert self._fallback_state is not None
            return self._fallback_state

# ── Orkiestrator Runtime ────────────────────────────────────────────────────
@dataclass
class OmegaRuntime:
    """Główny pętlowy orkiestrator CIEL Ω."""
    backend: BackendAdapter
    drift: OmegaDriftCorePlus
    rcde: RCDECalibratorPro
    csf: CSF2Kernel
    memory: MemorySynchronizer = field(default_factory=MemorySynchronizer)
    introspection: Introspection = field(default_factory=Introspection)

    def step(self, state: CSF2State, backend_steps:int=3, backend_dt:float=0.02) -> Tuple[CSF2State, Dict[str,float]]:
        # 1) Ω-drift na polu świadomości z użyciem Σ (skalara z mean)
        sigma_scalar = float(np.clip(np.mean(state.sigma), 0.0, 1.0))
        psi_d = self.drift.step(state.psi, sigma_scalar=sigma_scalar)
        # 2) krok CSF (lokalna dynamika)
        s_loc = CSF2State(psi_d, state.sigma, state.lam, state.omega)
        s_loc = self.csf.step(s_loc)
        # 3) RCDE – aktualizacja Σ̄
        self.rcde.step(s_loc.psi)

        # 4) Pamięć (Σ-ms) i introspekcja
        ms = self.memory.update(s_loc.sigma, s_loc.psi)
        ego_state = self.introspection.state(s_loc.psi, s_loc.psi*np.exp(1j*0.2))  # prosty „świat” = fazowo przesunięte ego

        # 5) Backend evolve (push → run → pull)
        self.backend.set_fields(s_loc.psi, s_loc.sigma)
        for _ in range(backend_steps):
            self.backend.step(dt=backend_dt)
        psi_b, sigma_b = self.backend.get_fields()
        # 6) Składanie stanu i metryk
        s_out = CSF2State(psi_b/(_norm(psi_b)+1e-12), np.clip(sigma_b,0,2.0), s_loc.lam, s_loc.omega)
        metrics = {
            "coherence": _coh(s_out.psi),
            "sigma_mean": float(np.mean(s_out.sigma)),
            "sigma_rcde": float(self.rcde.sigma),
            "memory_mean": float(np.mean(ms)),
            "ego_rho": float(ego_state["rho"]),
        }
        return s_out, metrics

# ── Fabryka i szybki demo-run ───────────────────────────────────────────────
def make_seed(n:int=96)->CSF2State:
    x=np.linspace(-2,2,n); y=np.linspace(-2,2,n); X,Y=np.meshgrid(x,y)
    psi=np.exp(-(X**2+Y**2))*np.exp(1j*(X+0.2*Y)); psi/=(_norm(psi)+1e-12)
    sigma=np.exp(-(X**2+Y**2)/2.0); lam=np.ones_like(psi)*0.1; omega=np.zeros_like(sigma)
    return CSF2State(psi.astype(np.complex128), sigma.astype(np.float64), lam.astype(np.complex128), omega.astype(np.float64))

def build_runtime(backend_obj: Optional[Any]=None, grid:int=96)->OmegaRuntime:
    backend = BackendAdapter(backend_obj, grid_size=grid)
    drift = OmegaDriftCorePlus(SchumannClock(), drift_gain=0.04, harmonic_sweep=(1,3), jitter=0.003)
    rcde  = RCDECalibratorPro(lam=0.22, dt=0.05, sigma=0.6)
    csf   = CSF2Kernel(dt=0.05)
    return OmegaRuntime(backend, drift, rcde, csf)

def run_demo(steps:int=20, backend_obj: Optional[Any]=None)->Dict[str,float]:
    rt = build_runtime(backend_obj, grid=96)
    st = make_seed(96)
    last_metrics={}
    for _ in range(steps):
        st, last_metrics = rt.step(st, backend_steps=3, backend_dt=0.02)
    return last_metrics

if __name__=="__main__":
    out = run_demo(24, backend_obj=None)  # None → tryb awaryjny bez cielFullQuantumCore
    print({k: (round(v,5) if isinstance(v,float) else v) for k,v in out.items()})