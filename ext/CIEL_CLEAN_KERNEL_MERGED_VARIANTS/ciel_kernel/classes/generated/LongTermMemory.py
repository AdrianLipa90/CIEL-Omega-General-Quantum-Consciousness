from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Callable
import numpy as np, time, math, threading, json, hashlib, queue, random

class LongTermMemory:
    """Lekka pamięć epizodyczna – nic nie zapisuje na dysk, ale potrafi serializować."""
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def put(self, label: str, psi: np.ndarray, sigma: float, meta: Optional[Dict[str, Any]]=None):
        payload = {'label': label, 'sigma': float(sigma), 'shape': psi.shape, 'psi_real': psi.real.astype(np.float32).tolist(), 'psi_imag': psi.imag.astype(np.float32).tolist(), 'meta': meta or {}}
        payload['hash'] = hashlib.sha256(json.dumps(payload['psi_real'][:64]).encode()).hexdigest()[:16]
        self.entries.append(payload)

    def export_json(self) -> str:
        return json.dumps(self.entries, ensure_ascii=False)

    def load_json(self, data: str):
        self.entries = json.loads(data)

    def restore(self, idx: int=-1) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        e = self.entries[idx]
        re = np.array(e['psi_real'], dtype=np.float32).reshape(e['shape'])
        im = np.array(e['psi_imag'], dtype=np.float32).reshape(e['shape'])
        psi = (re + 1j * im).astype(np.complex128)
        return (psi, float(e['sigma']), e.get('meta', {}))