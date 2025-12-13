from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

class ExpRegistry:
    exps: Dict[str, ExpFn] = field(default_factory=dict)

    def add(self, name: str, fn: ExpFn):
        self.exps[name] = fn

    def run(self, names: List[str]) -> Dict[str, Dict[str, Any]]:
        out = {}
        for n in names:
            if n in self.exps:
                out[n] = self.exps[n]()
        return out