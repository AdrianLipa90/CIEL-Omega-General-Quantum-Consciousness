"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Ethical memory logger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any

import json
import time


@dataclass(slots=True)
class EthicsLogger:
    path: Path
    history: list[Dict[str, Any]] = field(default_factory=list, init=False, repr=False)

    def record(self, entry: Dict[str, Any]) -> None:
        payload = dict(entry, timestamp=time.time())
        self.history.append(payload)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with Path(self.path).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


__all__ = ["EthicsLogger"]
