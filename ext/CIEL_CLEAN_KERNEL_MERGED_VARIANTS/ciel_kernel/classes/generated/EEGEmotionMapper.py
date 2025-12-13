from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

class EEGEmotionMapper:
    """
    Minimalny mapper z pasm EEG (delta..gamma) na składowe emocji.
    Oczekuje słownika: {"delta":..,"theta":..,"alpha":..,"beta":..,"gamma":..}
    """
    alpha_calm_gain: float = 1.0
    beta_focus_gain: float = 1.0
    gamma_stress_gain: float = 1.0
    theta_awe_gain: float = 0.8
    delta_sad_gain: float = 0.5

    def map(self, bands: Dict[str, float]) -> Dict[str, float]:
        alpha = float(bands.get('alpha', 0.0))
        beta = float(bands.get('beta', 0.0))
        gamma = float(bands.get('gamma', 0.0))
        theta = float(bands.get('theta', 0.0))
        delta = float(bands.get('delta', 0.0))
        calm = np.tanh(self.alpha_calm_gain * alpha)
        focus = np.tanh(self.beta_focus_gain * beta)
        stress = np.tanh(self.gamma_stress_gain * gamma)
        awe = np.tanh(self.theta_awe_gain * theta)
        sad = np.tanh(self.delta_sad_gain * delta)
        joy = np.clip(0.6 * calm + 0.4 * focus - 0.3 * stress, 0.0, 1.0)
        return {'joy': float(joy), 'calm': float(calm), 'awe': float(awe), 'stress': float(stress), 'sadness': float(sad), 'anger': float(np.clip(0.5 * stress - 0.2 * calm, 0.0, 1.0))}