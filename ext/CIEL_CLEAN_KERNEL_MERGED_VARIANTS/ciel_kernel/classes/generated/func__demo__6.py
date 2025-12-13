from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

def _demo():
    monitor = EthicalMonitor()
    for c in np.linspace(0.1, 1.0, 6):
        val, col = monitor.evaluate_and_color(c, intention=0.8, mass=0.5)
        print(f'coh={c:.2f} → ethics={val:.3f}, color={col}, decay={ethical_decay(val):.3f}')