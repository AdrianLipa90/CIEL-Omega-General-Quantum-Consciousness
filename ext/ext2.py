# -*- coding: utf-8 -*-
"""
CIEL/0 – Batch Pack (no-FFT edition)
Zestawiony z: Ciel CSF.txt, rcde_calibrated.py, ciel_quantum_optimiser.py,
noweparadoxy.py, cielfullyfull.py
Wersja całkowicie wektoryzowana, bez transformacji Fouriera.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

# ---------------------------------------------------------------------
# 1) CSF SIMULATOR  –  pole świadomości Ψ(x,t) w przestrzeni realnej
# ---------------------------------------------------------------------
@dataclass
class CSFSimulator:
    size: int = 128
    sigma: float = 2.0
    dt: float = 0.01
    smooth_strength: float = 0.15
    seed: Optional[int] = None

    X: np.ndarray = field(init=False, repr=False)
    Y: np.ndarray = field(init=False, repr=False)
    psi: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        if self.seed is not None:
            np.random.seed(self.seed)
        x = np.linspace(-3.0, 3.0, self.size)
        y = np.linspace(-3.0, 3.0, self.size)
        self.X, self.Y = np.meshgrid(x, y)
        env = np.exp(-(self.X**2 + self.Y**2) / (self.sigma**2))
        phase = np.exp(1j * (self.X + self.Y))
        self.psi = env * phase

    @staticmethod
    def _smooth2d(a: np.ndarray, k: int = 1) -> np.ndarray:
        """prosty filtr pudełkowy – bez FFT"""
        if k <= 0:
            return a
        out = a.copy()
        for _ in range(k):
            tmp = np.pad(out, ((1, 1), (1, 1)), mode="reflect")
            out = (tmp[1:-1,1:-1] + tmp[0:-2,1:-1] + tmp[2:,1:-1]
                   + tmp[1:-1,0:-2] + tmp[1:-1,2:]) / 5.0
        return out

    def step(self, n: int = 1, drift: float = 1.0) -> None:
        """Iteracyjna ewolucja w domenie realnej."""
        for _ in range(n):
            gy = np.zeros_like(self.psi)
            gx = np.zeros_like(self.psi)
            gy[1:-1,:] = 0.5*(self.psi[2:,:] - self.psi[:-2,:])
            gx[:,1:-1] = 0.5*(self.psi[:,2:] - self.psi[:,:-2])
            self.psi += 1j*self.dt*drift*(gy+gx)
            s_real = self._smooth2d(self.psi.real)
            s_imag = self._smooth2d(self.psi.imag)
            self.psi = (1-self.smooth_strength)*self.psi + self.smooth_strength*(s_real+1j*s_imag)
            self.psi /= np.sqrt(np.mean(np.abs(self.psi)**2))+1e-12

# ---------------------------------------------------------------------
# 2) RCDE – rezonans i kalibracja
# ---------------------------------------------------------------------
class RCDECalibrated:
    @staticmethod
    def normalize_field(field: np.ndarray) -> np.ndarray:
        return field / (np.sqrt(np.mean(np.abs(field)**2)) + 1e-12)

    @staticmethod
    def compute_resonance_index(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.mean(np.abs(a * np.conj(b))))

    @staticmethod
    def calibrate(reference_field: np.ndarray, test_field: np.ndarray) -> float:
        ref = RCDECalibrated.normalize_field(reference_field)
        tst = RCDECalibrated.normalize_field(test_field)
        return float(np.tanh(RCDECalibrated.compute_resonance_index(ref, tst)))

# ---------------------------------------------------------------------
# 3) PARADOXY – wersje realne (bez FFT)
# ---------------------------------------------------------------------
class IdentityDriftParadox:
    def resolve(self, psi: np.ndarray, S: np.ndarray) -> np.ndarray:
        delta = np.mean(np.abs(psi - S))
        w = 1.0 - np.exp(-delta)
        return (1.0 - w)*psi + w*S

class TemporalEchoParadox:
    def resolve(self, prev: np.ndarray, curr: np.ndarray, alpha: float = 0.1) -> np.ndarray:
        return curr + alpha*(curr - prev)

class InformationMirrorParadox:
    """Zamiast FFT – lokalny filtr kontrastu fazowego"""
    def resolve(self, psi: np.ndarray, beta: float = 0.05) -> np.ndarray:
        # oblicz lokalną „ostrość” pola
        gx = np.zeros_like(psi)
        gy = np.zeros_like(psi)
        gx[:,1:-1] = psi[:,2:] - psi[:,:-2]
        gy[1:-1,:] = psi[2:,:] - psi[:-2,:]
        sharp = np.sqrt(np.abs(gx)**2 + np.abs(gy)**2)
        boost = 1 + beta*(sharp / (np.max(sharp)+1e-12))
        psi_new = psi * boost
        psi_new /= np.sqrt(np.mean(np.abs(psi_new)**2)) + 1e-12
        return psi_new

# ---------------------------------------------------------------------
# 4) QUANTUM OPTIMISER – bez zmian
# ---------------------------------------------------------------------
@dataclass
class QuantumOptimiser:
    lr: float = 0.05
    steps: int = 50
    ethical_weight: float = 1.0

    def optimize_constants(
        self,
        constants: Dict[str, float],
        metrics_fn: Callable[[Dict[str, float]], Tuple[float, float, bool]]
    ) -> Dict[str, float]:
        keys = list(constants.keys())
        for _ in range(self.steps):
            coh, fid, ok = metrics_fn(constants)
            loss = (1-coh)**2 + (1-fid)**2 + (0 if ok else 0.1*self.ethical_weight)
            grad={}
            eps=1e-3
            for k in keys:
                orig=constants[k]
                constants[k]=orig+eps
                coh2,fid2,ok2=metrics_fn(constants)
                loss2=(1-coh2)**2+(1-fid2)**2+(0 if ok2 else 0.1*self.ethical_weight)
                grad[k]=(loss2-loss)/eps
                constants[k]=orig
            for k in keys:
                constants[k]-=self.lr*grad[k]
        return constants

# ---------------------------------------------------------------------
# 5) ORCHESTRATOR – lite, no-FFT
# ---------------------------------------------------------------------
@dataclass
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
        hist = {"coherence": [], "calibration": [], "amplitude": []}
        prev = self.sim.psi.copy()
        S = np.abs(self.sim.psi)*np.exp(1j*(np.angle(self.sim.psi)+0.3))
        for _ in range(self.steps):
            self.sim.step(1)
            psi=self.sim.psi
            psi=self.idrift.resolve(psi,S)
            psi=self.techo.resolve(prev,psi,alpha=self.paradox_alpha)
            psi=self.imirr.resolve(psi,beta=self.paradox_beta)
            psi /= np.sqrt(np.mean(np.abs(psi)**2))+1e-12
            self.sim.psi=psi
            calib=RCDECalibrated.calibrate(S,psi)
            coh=float(np.mean(np.abs(psi*np.conj(S))))
            amp=float(np.sqrt(np.mean(np.abs(psi)**2)))
            hist["coherence"].append(coh)
            hist["calibration"].append(calib)
            hist["amplitude"].append(amp)
            prev=psi
        return hist

def _demo():
    k=CIELFullKernelLite(size=96,steps=80)
    h=k.run()
    print(f"mean coherence {np.mean(h['coherence']):.4f}")
    print(f"mean calibration {np.mean(h['calibration']):.4f}")

if __name__=="__main__":
    _demo()