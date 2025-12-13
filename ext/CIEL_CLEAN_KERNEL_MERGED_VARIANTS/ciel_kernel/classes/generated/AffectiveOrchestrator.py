from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

class AffectiveOrchestrator:
    """
    Łączy:
      - EEGEmotionMapper  : EEG → wektor afektu
      - EmotionCore       : aktualizuje stany
      - Σ (sigma_scalar)  : moduluje „siłę” afektu
      - ColorMap (opcjonalnie): barwy dla UI/VR (jeśli dostępny)
    """
    mapper: EEGEmotionMapper = field(default_factory=EEGEmotionMapper)
    core: EmotionCore = field(default_factory=EmotionCore)
    use_color: bool = True
    _ColorMap: Any = field(default=None, init=False, repr=False)

    def _maybe_color(self):
        if not self.use_color or self._ColorMap is not None:
            return
        try:
            from ColorMap import ColorMap as _CM
            self._ColorMap = _CM
        except Exception:

            class _Fallback:

                @staticmethod
                def map_value(v: float) -> Tuple[float, float, float]:
                    v = float(np.clip(v, 0.0, 1.0))
                    return (0.2 * (1 - v) + 1.0 * v, 0.4 * (1 - v) + 1.0 * v, 0.9 * (1 - v) + 0.95 * v)
            self._ColorMap = _Fallback

    def step(self, eeg_bands: Dict[str, float], sigma_scalar: float=1.0, psi_field: Optional[np.ndarray]=None, coherence_field: Optional[np.ndarray]=None) -> Dict[str, Any]:
        """
        - eeg_bands      : moce pasm EEG (np. z EEGProcessor)
        - sigma_scalar   : skalar Σ̄(t) (np. z UnifiedSigmaField)
        - psi_field      : opcjonalne pole (do obliczenia intensywności)
        - coherence_field: opcjonalna mapa koherencji (0..1)
        Zwraca: pakiet afektywny + kolor (jeśli dostępny)
        """
        affect_vec = self.mapper.map(eeg_bands)
        mod_affect = {k: float(np.clip(v * sigma_scalar, 0.0, 1.0)) for k, v in affect_vec.items()}
        emo_state = self.core.update(mod_affect)
        mood = self.core.summary_scalar()
        field_out = None
        if psi_field is not None and coherence_field is not None:
            intensity = np.abs(psi_field)
            field_out = FeelingField(gain=1.0).build(intensity=intensity, coherence=coherence_field)
        self._maybe_color()
        color = self._ColorMap.map_value(mood) if self.use_color else None
        return {'affect_vector': affect_vec, 'affect_modulated': mod_affect, 'emotion_state': emo_state, 'mood_scalar': float(mood), 'affect_field': field_out, 'color': color}