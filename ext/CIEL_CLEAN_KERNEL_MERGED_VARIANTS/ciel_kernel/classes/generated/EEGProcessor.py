from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional
import numpy as np
import threading, queue, time

class EEGProcessor:
    fs: float = 256.0
    bands: Dict[str, tuple] = field(default_factory=lambda: {'delta': (0.5, 4.0), 'theta': (4.0, 8.0), 'alpha': (8.0, 12.0), 'beta': (12.0, 30.0), 'gamma': (30.0, 45.0)})
    window_size: int = 256

    def power_band(self, signal: np.ndarray, band: tuple) -> float:
        """Moc pasma przez filtrację różnicową (bez FFT)."""
        low, high = band
        dt = 1.0 / self.fs
        t = np.arange(len(signal)) * dt
        f = np.sin(2 * np.pi * ((low + high) / 2) * t)
        return float(np.mean((signal * f) ** 2))

    def analyze(self, signal: np.ndarray) -> Dict[str, float]:
        """Zwraca moce pasm i koherencję między nimi."""
        results = {k: self.power_band(signal, v) for k, v in self.bands.items()}
        vals = np.array(list(results.values()))
        coherence = float(np.mean(vals / (np.max(vals) + 1e-12)))
        results['coherence'] = coherence
        return results