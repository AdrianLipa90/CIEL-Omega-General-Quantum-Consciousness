from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class EthicsGuard:
    """Lekki strażnik: szybka kontrola metryk względem polityki życia."""

    def __init__(self, bound: float=0.9, min_coh: float=0.4, block: bool=True):
        self.ethical_bound = float(bound)
        self.min_coherence = float(min_coh)
        self.block = bool(block)

    def check_step(self, coherence: float, ethical_ok: bool, info_fidelity: float) -> None:
        if coherence < self.min_coherence or not ethical_ok:
            msg = f'[EthicsGuard] breach: coherence={coherence:.3f} ethical_ok={ethical_ok} fidelity={info_fidelity:.3f}'
            if self.block:
                raise RuntimeError(msg)
            else:
                print('⚠', msg)