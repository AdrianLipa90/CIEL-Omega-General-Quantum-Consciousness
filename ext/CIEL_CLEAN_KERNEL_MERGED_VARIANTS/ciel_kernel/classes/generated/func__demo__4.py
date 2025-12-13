from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

def _demo():
    k = CIELFullKernelLite(size=96, steps=80)
    h = k.run()
    print(f"mean coherence {np.mean(h['coherence']):.4f}")
    print(f"mean calibration {np.mean(h['calibration']):.4f}")