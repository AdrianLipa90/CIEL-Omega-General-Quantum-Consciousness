from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class RealityLogger:
    """Logger w formacie JSONL (przyjazny narzędziom)."""

    def __init__(self, path: str='logs/reality.jsonl'):
        self.path = path
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)

    def record(self, step: int, metrics: Dict[str, Any]) -> None:
        rec = dict(step=step, t=time.time(), **metrics)
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')