from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List

class SimConfig:
    channels: int = 12
    sample_rate: float = 128.0
    duration: float = 1.0