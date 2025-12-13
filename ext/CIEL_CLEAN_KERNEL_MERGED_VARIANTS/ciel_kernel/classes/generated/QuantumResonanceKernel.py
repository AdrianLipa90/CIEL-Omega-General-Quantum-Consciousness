from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional
import numpy as np
import threading, queue, time

class QuantumResonanceKernel:
    """Ewolucja rezonansowa pola intencji I(x,t)"""
    physics: CIELPhysics = field(default_factory=CIELPhysics)
    coherence_threshold: float = 0.8

    def resonance(self, S: np.ndarray, I: np.ndarray) -> float:
        """Oblicza rezonans między stanem symbolicznym S a intencją I."""
        inner = np.vdot(S, I)
        return float(np.abs(inner) ** 2)

    def is_coherent(self, resonance: float) -> bool:
        return resonance >= self.coherence_threshold

    def evolve_step(self, psi: np.ndarray, potential: Optional[np.ndarray]=None, dt: float=0.01) -> np.ndarray:
        """
        Ewoluuje pole Ψ(t) przez prostą iterację Laplasjanu (no-FFT)
        z opcjonalnym potencjałem V(x).
        """
        lap = np.zeros_like(psi, dtype=psi.dtype)
        lap[1:-1, 1:-1] = psi[2:, 1:-1] + psi[:-2, 1:-1] + psi[1:-1, 2:] + psi[1:-1, :-2] - 4 * psi[1:-1, 1:-1]
        next_psi = psi + 1j * dt * lap
        if potential is not None:
            next_psi -= 1j * dt * potential * psi
        norm = np.sqrt(np.mean(np.abs(next_psi) ** 2)) + 1e-12
        return next_psi / norm

    def integrate(self, F: np.ndarray) -> np.ndarray:
        """Numeryczna całka krokowa (trapezowa light)."""
        return np.cumsum(F)

    def field_energy(self, psi: np.ndarray) -> float:
        """Oblicza gęstość energii pola (znormalizowaną)."""
        grad_y = np.zeros_like(psi)
        grad_x = np.zeros_like(psi)
        grad_y[1:-1, :] = psi[2:, :] - psi[:-2, :]
        grad_x[:, 1:-1] = psi[:, 2:] - psi[:, :-2]
        E = np.mean(np.abs(grad_x) ** 2 + np.abs(grad_y) ** 2)
        return float(E)

    def metrics(self, psi: np.ndarray, ref: np.ndarray) -> Dict[str, float]:
        """Zwraca pakiet metryk: rezonans, energia, fiducja."""
        res = self.resonance(psi, ref)
        energy = self.field_energy(psi)
        fid = float(np.mean(np.abs(np.conj(psi) * ref)))
        return {'resonance': res, 'energy': energy, 'fidelity': fid}