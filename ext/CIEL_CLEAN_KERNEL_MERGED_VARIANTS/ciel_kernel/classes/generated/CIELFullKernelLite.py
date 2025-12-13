from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

class CIELFullKernelLite:
    size: int = 128
    steps: int = 200
    dt: float = 0.01
    paradox_alpha: float = 0.1
    paradox_beta: float = 0.05
    sim: CSFSimulator = field(init=False, repr=False)
    idrift: IdentityDriftParadox = field(default_factory=IdentityDriftParadox, repr=False)
    techo: TemporalEchoParadox = field(default_factory=TemporalEchoParadox, repr=False)
    imirr: InformationMirrorParadox = field(default_factory=InformationMirrorParadox, repr=False)

    def __post_init__(self):
        self.sim = CSFSimulator(size=self.size, dt=self.dt)

    def run(self) -> Dict[str, List[float]]:
        hist = {'coherence': [], 'calibration': [], 'amplitude': []}
        prev = self.sim.psi.copy()
        S = np.abs(self.sim.psi) * np.exp(1j * (np.angle(self.sim.psi) + 0.3))
        for _ in range(self.steps):
            self.sim.step(1)
            psi = self.sim.psi
            psi = self.idrift.resolve(psi, S)
            psi = self.techo.resolve(prev, psi, alpha=self.paradox_alpha)
            psi = self.imirr.resolve(psi, beta=self.paradox_beta)
            psi /= np.sqrt(np.mean(np.abs(psi) ** 2)) + 1e-12
            self.sim.psi = psi
            calib = RCDECalibrated.calibrate(S, psi)
            coh = float(np.mean(np.abs(psi * np.conj(S))))
            amp = float(np.sqrt(np.mean(np.abs(psi) ** 2)))
            hist['coherence'].append(coh)
            hist['calibration'].append(calib)
            hist['amplitude'].append(amp)
            prev = psi
        return hist