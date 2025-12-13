from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class CielConfig:
    """Parametry uruchomieniowe przenoszone poza kod."""
    enable_gpu: bool = True
    enable_numba: bool = True
    log_path: str = 'logs/reality.jsonl'
    ethics_min_coherence: float = 0.4
    ethics_block_on_violation: bool = True
    dataset_path: Optional[str] = None