from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import datetime, json, os, time, requests, sys, subprocess

class MemoryLog:
    """Structured memory journal with ethical tagging."""

    def __init__(self, path: str='ciel_memory.jsonl'):
        self.path = path
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)

    def record(self, entry: Dict[str, Any]):
        entry['timestamp'] = datetime.datetime.utcnow().isoformat()
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def log_event(self, name: str, ethical: bool, value: float):
        self.record({'event': name, 'ethical': ethical, 'value': value})

    def summarize(self) -> Dict[str, float]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, 'r', encoding='utf-8') as f:
            lines = [json.loads(x) for x in f]
        values = [l['value'] for l in lines if 'value' in l]
        return {'mean_value': float(np.mean(values)) if values else 0.0}