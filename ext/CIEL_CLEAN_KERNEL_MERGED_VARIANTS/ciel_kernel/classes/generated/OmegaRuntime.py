from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List, Callable
import numpy as np, math, time

class OmegaRuntime:
    """Główny pętlowy orkiestrator CIEL Ω."""
    backend: BackendAdapter
    drift: OmegaDriftCorePlus
    rcde: RCDECalibratorPro
    csf: CSF2Kernel
    memory: MemorySynchronizer = field(default_factory=MemorySynchronizer)
    introspection: Introspection = field(default_factory=Introspection)

    def step(self, state: CSF2State, backend_steps: int=3, backend_dt: float=0.02) -> Tuple[CSF2State, Dict[str, float]]:
        sigma_scalar = float(np.clip(np.mean(state.sigma), 0.0, 1.0))
        psi_d = self.drift.step(state.psi, sigma_scalar=sigma_scalar)
        s_loc = CSF2State(psi_d, state.sigma, state.lam, state.omega)
        s_loc = self.csf.step(s_loc)
        self.rcde.step(s_loc.psi)
        ms = self.memory.update(s_loc.sigma, s_loc.psi)
        ego_state = self.introspection.state(s_loc.psi, s_loc.psi * np.exp(1j * 0.2))
        self.backend.set_fields(s_loc.psi, s_loc.sigma)
        for _ in range(backend_steps):
            self.backend.step(dt=backend_dt)
        psi_b, sigma_b = self.backend.get_fields()
        s_out = CSF2State(psi_b / (_norm(psi_b) + 1e-12), np.clip(sigma_b, 0, 2.0), s_loc.lam, s_loc.omega)
        metrics = {'coherence': _coh(s_out.psi), 'sigma_mean': float(np.mean(s_out.sigma)), 'sigma_rcde': float(self.rcde.sigma), 'memory_mean': float(np.mean(ms)), 'ego_rho': float(ego_state['rho'])}
        return (s_out, metrics)