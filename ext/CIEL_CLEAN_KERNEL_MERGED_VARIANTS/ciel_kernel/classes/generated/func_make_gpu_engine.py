from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

def make_gpu_engine(cfg: Optional[CielConfig]=None) -> GPUEngine:
    cfg = cfg or CielConfig()
    return GPUEngine(enable_gpu=cfg.enable_gpu, enable_numba=cfg.enable_numba)