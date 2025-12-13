from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import numpy as np

def _demo():
    n = 96
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.5 * Y))
    L = Lie4MatrixEngine()
    basis = L.basis_so31()
    keys = sorted(basis.keys())
    C01_02 = L.commutator(basis[0, 1], basis[0, 2])
    lie_sig = float(np.linalg.norm(C01_02))
    sigma = SigmaSeries(alpha=0.7, sigma0=0.4, steps=128)
    psi1 = sigma.apply_to_field(psi0)
    psi2 = ParadoxFilters.twin_identity(psi1)
    psi3 = ParadoxFilters.echo(prev=psi1, curr=psi2, k=0.1)
    psi4 = ParadoxFilters.boundary_collapse(psi3, tol=0.001)
    vis = VisualCore(clip_amp=99.0)
    T = vis.tensorize(psi4)
    print('LIE₄ basis size:', len(basis))
    print('‖[M01, M02]‖ =', f'{lie_sig:.4f}')
    print('SigmaSeries last Σ:', f'{sigma.run()[-1]:.4f}')
    print('Visual tensor shape:', T.shape)