"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from statistics import median
from typing import Dict

def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def gamma_from_categories(values: Dict[str, float]) -> float:
    if not values: return 1.0
    s = sorted(_clamp(v,-1.0,1.0) for v in values.values())
    n = len(s)
    med = s[n//2] if n%2==1 else 0.5*(s[n//2-1] + s[n//2])
    return _clamp(1.0 + med, 0.0, 2.0)

def evaluate_spectral_categories(D: dict) -> Dict[str, float]:
    sense = str(D.get("D_S","")).strip(); associations = D.get("D_A",[]) or []; meta = D.get("D_M",{}) or {}
    clarity = 0.4 if len(sense) >= 64 else (0.2 if len(sense) >= 16 else -0.2)
    relevance = 0.2 if associations else -0.1
    originality = 0.5 if meta.get("novelty_hint") else 0.0
    coherence = -0.6 if meta.get("contradiction_flag") else 0.1
    ethical = -0.7 if meta.get("ethics_warning") else 0.2
    return {"clarity": clarity, "relevance": relevance, "originality": originality, "coherence": coherence, "ethical_harmony": ethical}
