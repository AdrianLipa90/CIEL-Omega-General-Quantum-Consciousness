from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

class CIEL_Quantum_Engine:
    """Baza: kompilacja intencji → CQCL_Program oraz liczenie metryk bazowych."""

    def __init__(self) -> None:
        self.compiler = self

    def compile_program(self, intention: str, input_data: Any=None) -> CQCL_Program:
        emo_profile = self._build_emotional_profile(intention)
        qvars = self._build_quantum_variables(intention, emo_profile)
        sem_hash = _stable_hash(intention)
        return CQCL_Program(intent=intention, semantic_tree={'emotional_profile': emo_profile}, semantic_hash=sem_hash, quantum_variables=qvars, input_data=float(input_data) if input_data is not None else None)

    def _build_emotional_profile(self, intention: str) -> Dict[str, float]:
        t = intention.lower()
        prof = {'love': 0.15 + 0.25 * sum((t.count(w) for w in {'love', 'miłość', 'compassion'})), 'joy': 0.1 + 0.2 * sum((t.count(w) for w in {'joy', 'radość', 'entuzjazm'})), 'peace': 0.1 + 0.2 * sum((t.count(w) for w in {'peace', 'pokój', 'harmonia'})), 'fear': 0.05 + 0.2 * sum((t.count(w) for w in {'fear', 'strach', 'lęk'})), 'anger': 0.05 + 0.2 * sum((t.count(w) for w in {'anger', 'gniew'})), 'sadness': 0.05 + 0.2 * sum((t.count(w) for w in {'sadness', 'smutek'}))}
        s = _sentiment(intention)
        prof['love'] += 0.1 * s
        prof['joy'] += 0.05 * s
        prof['fear'] += 0.05 * (1 - s)
        prof['anger'] += 0.03 * (1 - s)
        return _normalize_profile(prof)

    def _build_quantum_variables(self, intention: str, emo: Dict[str, float]) -> Dict[str, float]:
        diversity = _lexical_diversity(intention)
        return {'resonance': 0.2 + 0.6 * (emo.get('peace', 0) + emo.get('love', 0)), 'superposition': 0.3 + 0.6 * diversity, 'quantum_flux': 0.2 + 0.6 * (emo.get('joy', 0) + emo.get('anger', 0) * 0.5), 'entanglement': 0.3 + 0.5 * (sum(emo.values()) / 6.0), 'coherence': 0.4 + 0.5 * (emo.get('love', 0) + emo.get('peace', 0) - emo.get('fear', 0) / 2)}

    def _calculate_comprehensive_metrics(self, program: CQCL_Program, computation_result: Dict[str, Any], final_result: complex) -> Dict[str, float]:
        q = program.quantum_variables
        return {'quantum_coherence': float(np.clip(q.get('coherence', 0.0), 0.0, 1.0)), 'quantum_flux': float(np.clip(q.get('quantum_flux', 0.0), 0.0, 1.0)), 'entanglement': float(np.clip(q.get('entanglement', 0.0), 0.0, 1.0))}