from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np

class PsychField:
    empathy: float = 0.7
    phase_lock: float = 0.2
    normalize: bool = True

    def _local_mean(self, a: np.ndarray) -> np.ndarray:
        """Lekki filtr pudełkowy 3×3 jako „empatyczne uśrednianie” sąsiedztwa."""
        tmp = np.pad(a, ((1, 1), (1, 1)), mode='reflect')
        return (tmp[1:-1, 1:-1] + tmp[0:-2, 1:-1] + tmp[2:, 1:-1] + tmp[1:-1, 0:-2] + tmp[1:-1, 2:]) / 5.0

    def interact(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Łączy dwa pola A i B w nowy stan C:
        - empatyczne domieszkowanie amplitud (mieszanka lokalnych średnich),
        - delikatny „phase-lock” (dopasowanie faz, bez FFT),
        - opcjonalna renormalizacja energii.
        """
        A = A.astype(np.complex128, copy=False)
        B = B.astype(np.complex128, copy=False)
        a_amp, b_amp = (np.abs(A), np.abs(B))
        a_ph, b_ph = (np.angle(A), np.angle(B))
        a_s, b_s = (self._local_mean(a_amp), self._local_mean(b_amp))
        amp_mix = (1.0 - self.empathy) * a_amp + self.empathy * b_s
        amp_mix = 0.5 * (amp_mix + ((1.0 - self.empathy) * b_amp + self.empathy * a_s))
        ph = (1.0 - self.phase_lock) * a_ph + self.phase_lock * b_ph
        C = amp_mix * np.exp(1j * ph)
        if self.normalize:
            C /= np.sqrt(np.mean(np.abs(C) ** 2)) + 1e-12
        return C

    def multi_interact(self, fields: Tuple[np.ndarray, ...]) -> np.ndarray:
        """
        Empatyczne „uśrednienie” wielu pól. Iteracyjnie łączy pary.
        """
        if not fields:
            raise ValueError('No fields provided')
        C = fields[0]
        for F in fields[1:]:
            C = self.interact(C, F)
        return C