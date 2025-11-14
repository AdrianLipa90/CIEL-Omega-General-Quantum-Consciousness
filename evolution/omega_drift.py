"""Phase drift core synchronised with the Schumann clock."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .schumann_clock import SchumannClock


def _field_norm(field: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.abs(field) ** 2)) + 1e-12)


@dataclass(slots=True)
class OmegaDriftCore:
    clock: SchumannClock
    drift_gain: float = 0.05
    harmonic: int = 1
    renorm: bool = True

    def step(self, psi: np.ndarray, sigma_scalar: float = 1.0) -> np.ndarray:
        carrier = self.clock.carrier(psi.shape, amp=1.0, k=self.harmonic)
        psi_next = psi * np.exp(1j * self.drift_gain * sigma_scalar) * carrier
        if self.renorm:
            psi_next /= _field_norm(psi_next)
        return psi_next


__all__ = ["OmegaDriftCore"]
