from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

def attach_ethics_and_logging(kernel: KernelSpec, cfg: Optional[CielConfig]=None):
    """
    Tworzy gotowe obiekty do ręcznego użycia w Twojej pętli.
    Nie zmienia kernela – pełna kontrola po Twojej stronie.
    """
    cfg = cfg or CielConfig()
    guard = EthicsGuard(bound=getattr(kernel.constants, 'ETHICAL_BOUND', 0.9), min_coh=cfg.ethics_min_coherence, block=cfg.ethics_block_on_violation)
    logger = RealityLogger(cfg.log_path)
    return (guard, logger)