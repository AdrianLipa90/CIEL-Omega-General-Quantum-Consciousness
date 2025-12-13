from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

def _demo():
    n = 64
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.3 * Y))
    sigma0 = np.exp(-(X ** 2 + Y ** 2) / 2.0)

    def psi_supplier(t: int):
        return psi0 * np.exp(1j * 0.05 * t)

    def sigma_supplier(t: int):
        return np.clip(sigma0 * (0.95 + 0.05 * np.cos(0.1 * t)), 0.0, 1.0)

    def options_supplier(t: int, intuition: float, prediction: float):
        base_ethic = 0.9
        return {'help': {'intent': max(0.0, intuition), 'ethic': base_ethic, 'confidence': 0.7 + 0.2 * prediction}, 'wait': {'intent': 0.4 + 0.3 * (1 - abs(intuition)), 'ethic': 0.8, 'confidence': 0.6}, 'risky': {'intent': 0.6 * prediction, 'ethic': 0.4 + 0.2 * t % 2, 'confidence': 0.5}}
    percept = PerceptiveLayer()
    cortex = IntuitiveCortex(entropy_map=np.ones(n * n))
    pred = PredictiveCore(tau=10.0)
    decide = DecisionCore(min_score=0.2)
    cog = CognitionOrchestrator(percept, cortex, pred, decide)
    logs = cog.run_cycle(steps=12, psi_supplier=psi_supplier, sigma_supplier=sigma_supplier, options_supplier=options_supplier)
    print('Last 3 steps:')
    for row in logs[-3:]:
        print(f"t={row['t']:02d}  intu={row['intuition']:.3f}  pred={row['prediction']:.3f}  choice={row['decision']}")