from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

def _demo():
    n = 96
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X ** 2 + Y ** 2)) * np.exp(1j * (X + 0.2 * Y))
    clk = SchumannClock()
    drift = OmegaDriftCorePlus(clk, drift_gain=0.04, harmonic_sweep=(1, 3), jitter=0.003)
    boot = OmegaBootRitual(drift, steps=12, intent_bias=0.1)
    out = boot.run(psi0, sigma0=0.55)
    print('Ω Boot:', {'sigma': round(out['sigma'], 4), 'coh': round(out['coherence'], 4)})
    rcde = RCDECalibratorPro(lam=0.22, dt=0.05, sigma=0.6)
    for _ in range(10):
        out['psi'] = out['psi'] + 1j * 0.01 * lap2(out['psi'])
        out['psi'] /= norm(out['psi'])
        rcde.step(out['psi'])
    print('RCDE Pro Σ:', round(rcde.sigma, 4))
    nodes = [NodeState('A', psi0.copy(), 0.5), NodeState('B', psi0 * np.exp(1j * 0.3), 0.6), NodeState('C', psi0 * np.exp(1j * 0.6), 0.55)]
    net = ResConnectParallel(nodes, drift_factory=lambda: OmegaDriftCorePlus(clk))
    for _ in range(5):
        net.step()
    print('ResConnect snapshot:', net.snapshot())
    da = DissociationAnalyzer()
    ego = psi0
    world = np.roll(psi0, 4, axis=1) * np.exp(1j * 0.25)
    diss = da.step(ego, world)
    print('Dissociation:', {'rho': round(diss['rho'], 4), 'state': diss['state']})
    ltm = LongTermMemory()
    ltm.put('post-boot', out['psi'], sigma=out['sigma'], meta={'coh': out['coherence']})
    js = ltm.export_json()
    psi_rest, sigma_rest, meta_rest = ltm.restore(-1)
    print('LTM:', {'len': len(ltm.entries), 'sigma_rest': round(sigma_rest, 4), 'meta': meta_rest})
    cl4 = ColatzLie4Engine(steps=64)
    inv = cl4.invariant(27)
    print('Collatz-LIE4 inv:', {k: round(v, 5) if isinstance(v, (int, float)) else v for k, v in inv.items()})