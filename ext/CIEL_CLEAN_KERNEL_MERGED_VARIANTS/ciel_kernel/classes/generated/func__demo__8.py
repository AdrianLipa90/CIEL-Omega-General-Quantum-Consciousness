from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np

def _demo():
    n = 96
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    seed = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.3 * Y))
    rex = RealityExpander(alpha=0.7, kappa=0.1, steps=12)
    psi_expanded = rex.expand(seed)
    usf = UnifiedSigmaField(shape=(n, n), omega=0.9, damping=0.03, dt=0.04)
    fields, scal = usf.evolve(T=32)
    pf = PsychField(empathy=0.65, phase_lock=0.25)
    C = pf.interact(seed, psi_expanded)
    print('Expanded field norm:', float(np.sqrt(np.mean(np.abs(psi_expanded) ** 2))))
    print('UnifiedSigmaField last Σ:', f'{scal[-1]:.4f}')
    print('PsychField mix norm:', float(np.sqrt(np.mean(np.abs(C) ** 2))))