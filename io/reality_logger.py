"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Log JSON lines for the simulated reality state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

import json
import time


@dataclass(slots=True)
class RealityLogger:
    path: Path

    def log(self, metrics: Dict[str, Any]) -> None:
        entry = dict(time=time.time(), **metrics)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with Path(self.path).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


__all__ = ["RealityLogger"]
