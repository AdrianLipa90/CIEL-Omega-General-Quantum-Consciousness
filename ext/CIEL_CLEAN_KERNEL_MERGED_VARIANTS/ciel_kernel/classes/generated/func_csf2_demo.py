from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List
import numpy as np, json, math

def csf2_demo(steps: int=20) -> Dict[str, float]:
    st = make_csf2_seed()
    ker = CSF2Kernel()
    mem = MemorySynchronizer()
    rep = CSFReporter()
    stress = ParadoxStress(0.06)
    for k in range(steps):
        st = ker.step(st)
        if k % 5 == 0:
            st = stress.apply(st)
        mem.update(st.sigma, st.psi)
    return rep.metrics(st)