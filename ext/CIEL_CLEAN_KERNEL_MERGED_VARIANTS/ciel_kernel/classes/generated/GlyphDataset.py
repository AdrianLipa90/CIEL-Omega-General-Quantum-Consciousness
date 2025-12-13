from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class GlyphDataset:
    """Prosty loader datasetów sygli (JSON → struktura wektorowa)."""
    path: str
    items: List[Dict[str, Any]] = field(default_factory=list)

    def load(self) -> 'GlyphDataset':
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.items = data if isinstance(data, list) else data.get('items', [])
        return self

    def to_vectors(self, key: str='features') -> np.ndarray:
        feats = [it.get(key, []) for it in self.items]
        maxlen = max((len(v) for v in feats), default=0)
        arr = np.zeros((len(feats), maxlen), dtype=float)
        for i, v in enumerate(feats):
            arr[i, :len(v)] = np.asarray(v, dtype=float)
        return arr