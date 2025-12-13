from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import datetime, json, os, time, requests, sys, subprocess

class CIELBatch3:
    """Unified high-level interface combining all batch3 components."""
    physics: CIELPhysics = field(default_factory=CIELPhysics)
    memory: MemoryLog = field(default_factory=MemoryLog)
    sigma_op: SoulInvariant = field(default_factory=SoulInvariant)
    loader: SimpleLoader = field(default_factory=SimpleLoader)

    def measure_and_log(self, field: np.ndarray, tag: str='default'):
        Σ = self.sigma_op.compute(field)
        self.memory.log_event(tag, ethical=Σ > 0.1, value=Σ)
        return Σ

    def summary(self) -> Dict[str, float]:
        return self.memory.summarize()