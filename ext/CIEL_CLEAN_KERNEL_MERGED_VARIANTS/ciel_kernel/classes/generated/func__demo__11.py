from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

def _demo():
    eeg_bands = {'alpha': 0.8, 'beta': 0.5, 'gamma': 0.3, 'theta': 0.4, 'delta': 0.2}
    n = 64
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.2 * Y))
    coh = np.clip(np.random.rand(n, n), 0.0, 1.0)
    orch = AffectiveOrchestrator()
    out = orch.step(eeg_bands, sigma_scalar=0.9, psi_field=psi, coherence_field=coh)
    print('Mood scalar:', round(out['mood_scalar'], 4))
    print('Emotion state:', {k: round(v, 3) for k, v in out['emotion_state'].items()})
    if out['color'] is not None:
        print('Color:', tuple((round(c, 3) for c in out['color'])))
    if out['affect_field'] is not None:
        print('Affect field shape:', out['affect_field'].shape)