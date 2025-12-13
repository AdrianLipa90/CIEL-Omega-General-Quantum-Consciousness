from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

class EmotionalCollatzEngine(CIEL_Quantum_Engine):
    """Silnik CQCL z rozszerzoną komputacją emocjonalną Collatza."""

    def __init__(self):
        super().__init__()
        self.emotional_operators = self._initialize_emotional_operators()

    def _initialize_emotional_operators(self) -> Dict[str, Dict[str, Any]]:
        return {'love': {'function': lambda n, intensity: n * (1 + intensity) if n % 2 == 0 else 3 * n + int(10 * intensity), 'description': 'Mnożenie przez miłość - ekspansja harmoniczna'}, 'fear': {'function': lambda n, intensity: max(1, int(n // max(1.0, 2 + intensity))) if n % 2 == 0 else max(1, n - int(5 * intensity)), 'description': 'Redukcja przez strach - kontrakcja ochronna'}, 'joy': {'function': lambda n, intensity: int(n // 2 + int(10 * intensity)) if n % 2 == 0 else 3 * n + int(20 * intensity), 'description': 'Eksplozja radości - wzmocniona kreatywność'}, 'anger': {'function': lambda n, intensity: int(n * (2 + intensity)) if n % 2 == 0 else 5 * n + int(15 * intensity), 'description': 'Mnożenie gniewu - intensyfikacja transformacji'}, 'peace': {'function': lambda n, intensity: max(1, int(n // max(1.0, 1 + intensity))) if n % 2 == 0 else n + 1, 'description': 'Wyciszenie pokoju - łagodna konwergencja'}, 'sadness': {'function': lambda n, intensity: max(1, n - int(3 * intensity)) if n % 2 == 0 else max(1, int(n // 2)), 'description': 'Redukcja smutku - spowolniona ewolucja'}}

    def emotional_collatz_transform(self, n: int, emotional_profile: Dict[str, float]) -> int:
        if n <= 1:
            return 1
        prof = _normalize_profile(emotional_profile)
        emotional_mix = 0.0
        total_w = 0.0
        for emotion, intensity in prof.items():
            if emotion in self.emotional_operators and intensity > 0.05:
                operator = self.emotional_operators[emotion]['function']
                emotional_mix += operator(n, intensity) * intensity
                total_w += intensity
        if total_w <= 1e-12:
            return n // 2 if n % 2 == 0 else 3 * n + 1
        return max(1, int(emotional_mix / total_w))

    def execute_emotional_program(self, intention: str, input_data: Any=None) -> Dict[str, Any]:
        program = self.compiler.compile_program(intention, input_data)
        emotional_path = self._generate_emotional_collatz_path(program)
        program.computation_path = emotional_path
        computation_result = self._execute_emotional_computation(program)
        final_result = self._apply_emotional_ramanujan_resonance(computation_result, program)
        metrics = self._calculate_emotional_metrics(program, computation_result, final_result)
        return {'program': program, 'computation_result': computation_result, 'final_result': final_result, 'metrics': metrics, 'emotional_landscape': self._analyze_emotional_landscape(program, emotional_path)}

    def _generate_emotional_collatz_path(self, program: CQCL_Program) -> List[int]:
        emotional_profile = dict(program.semantic_tree['emotional_profile'])
        seed = program.semantic_hash % 10000 + 1
        current, path, max_iterations = (seed, [], 300)
        iter_no = 0
        while current != 1 and iter_no < max_iterations:
            path.append(current)
            current = self.emotional_collatz_transform(current, emotional_profile)
            if iter_no % 10 == 0:
                emotional_profile = self._evolve_emotional_profile(emotional_profile, iter_no)
            iter_no += 1
        path.append(1)
        return path

    def _evolve_emotional_profile(self, profile: Dict[str, float], iteration: int) -> Dict[str, float]:
        evolution_factor = float(np.sin(iteration * 0.1) * 0.1 + 1.0)
        evolved = {}
        for emotion, intensity in profile.items():
            fluct = float(np.clip(np.random.normal(1.0, 0.1), 0.7, 1.3))
            evolved[emotion] = max(0.0, min(1.0, intensity * evolution_factor * fluct))
        return _normalize_profile(evolved)

    def _execute_emotional_computation(self, program: CQCL_Program) -> Dict[str, Any]:
        path = program.computation_path
        qv = program.quantum_variables
        emo_prof = dict(program.semantic_tree['emotional_profile'])
        interm, emo_amps, coh_hist = ([], [], [])
        current_state = complex(program.input_data or 1.0, 0.0)
        resonance = float(np.clip(qv['resonance'], 0.0, 1.0))
        superpos = float(np.clip(qv['superposition'], 0.0, 1.0))
        qflux = float(np.clip(qv['quantum_flux'], 0.0, 1.0))
        ent = float(np.clip(qv['entanglement'], 0.0, 1.0))
        base_coh = float(np.clip(qv['coherence'], 0.0, 1.0))
        for step, cn in enumerate(path):
            emo_intensity = sum(emo_prof.values()) / (len(emo_prof) or 1)
            if cn % 2 == 0:
                reduction_base = max(1.0, math.sqrt(cn))
                emo_mod = 1.0 + 0.5 * emo_intensity
                phase = np.exp(1j * resonance * step * emo_mod)
                current_state *= reduction_base * phase * emo_mod
            else:
                expansion_base = max(1.0, cn ** (superpos * (0.5 + emo_intensity)))
                fluct = np.exp(1j * qflux * step * (1 + emo_intensity))
                current_state *= expansion_base * fluct
            if step % 5 == 0:
                entang = 0j
                for emotion, intensity in emo_prof.items():
                    ph = hashlib.sha1(emotion.encode()).digest()[0] % 100 / 100.0 * math.pi
                    entang += intensity * np.exp(1j * ph)
                current_state += entang * ent * 0.1
            interm.append(current_state)
            emo_amps.append(abs(current_state) * (1 + emo_intensity))
            coh_hist.append(base_coh * (0.9 + 0.1 * emo_intensity) ** step)
            program.execution_trace.append({'step': step, 'collatz_number': cn, 'state': current_state, 'amplitude': abs(current_state), 'emotional_intensity': emo_intensity, 'emotional_profile': dict(emo_prof)})
        return {'final_state': current_state, 'intermediate_states': interm, 'emotional_amplitudes': emo_amps, 'coherence_history': coh_hist, 'path_length': len(path), 'max_emotional_amplitude': max(emo_amps) if emo_amps else 0.0, 'emotional_convergence': self._calculate_emotional_convergence(emo_amps)}

    def _calculate_emotional_convergence(self, amplitudes: List[float]) -> float:
        if len(amplitudes) < 2:
            return 0.0
        var = float(np.var(amplitudes) / (np.mean(amplitudes) + 1e-10))
        stability = 1.0 / (1.0 + var)
        if len(amplitudes) > 15:
            x = np.arange(len(amplitudes), dtype=float)
            slope = float(np.polyfit(x, amplitudes, 1)[0]) if len(amplitudes) >= 2 else 0.0
            trend_stability = 1.0 / (1.0 + abs(slope))
        else:
            trend_stability = 0.5
        return (stability + trend_stability) / 2.0

    def _apply_emotional_ramanujan_resonance(self, result: Dict[str, Any], program: CQCL_Program) -> complex:
        raw = result['final_state']
        emo = program.semantic_tree['emotional_profile']
        corr = 1.0
        for emotion, intensity in emo.items():
            h = hashlib.blake2b(emotion.encode(), digest_size=2).digest()[0] / 255.0
            corr *= 1.0 + intensity * h * 0.1
        emo_phase = sum((intensity * (hashlib.sha1(em.encode()).digest()[0] % 100) / 100.0 for em, intensity in emo.items()))
        phase = np.exp(1j * 2 * np.pi * (emo_phase / max(1, len(emo))))
        return raw * corr * phase

    def _calculate_emotional_metrics(self, program: CQCL_Program, computation_result: Dict[str, Any], final_result: complex) -> Dict[str, float]:
        base = super()._calculate_comprehensive_metrics(program, computation_result, final_result)
        emo = program.semantic_tree['emotional_profile']
        emo_vals = list(emo.values())
        emotional_balance = 1.0 - abs(emo.get('love', 0) - emo.get('fear', 0))
        emotional_diversity = len([v for v in emo_vals if v > 0.1]) / max(1, len(emo_vals))
        emotional_intensity = sum(emo_vals) / max(1, len(emo_vals))
        emotional_coherence = float(computation_result['emotional_convergence'])
        base.update({'emotional_coherence': emotional_coherence, 'emotional_intensity': emotional_intensity, 'emotional_diversity': emotional_diversity, 'emotional_balance': emotional_balance, 'heart_mind_coherence': base['quantum_coherence'] * emotional_coherence})
        return base

    def _analyze_emotional_landscape(self, program: CQCL_Program, path: List[int]) -> Dict[str, Any]:
        emo = program.semantic_tree['emotional_profile']
        dominant = max(emo.items(), key=lambda x: x[1])[0] if emo else 'none'
        changes = np.diff(path) if len(path) > 1 else np.array([])
        if len(changes) > 0:
            growth = int(np.sum(changes > 0))
            decay = int(np.sum(changes < 0))
            if growth > 2 * decay:
                pat = 'EKSPANSJA_EMOCJONALNA'
            elif decay > 2 * growth:
                pat = 'KONTRAKCJA_EMOCJONALNA'
            else:
                pat = 'RÓWNOWAGA_EMOCJONALNA'
        else:
            pat = 'BRAK_WZORCA'
        peaks = 0
        if len(path) > 2:
            for i in range(1, len(path) - 1):
                if path[i - 1] < path[i] > path[i + 1]:
                    peaks += 1
        if peaks > len(path) // 10:
            pattern_list = [pat, 'CYKLICZNOŚĆ_EMOCJONALNA']
        else:
            pattern_list = [pat]
        return {'dominant_emotion': dominant, 'emotional_complexity': len([v for v in emo.values() if v > 0.2]), 'path_emotional_signature': int(_stable_hash(str(tuple(path))) % 10000), 'emotional_operators_used': [e for e, v in emo.items() if v > 0.3 and e in self.emotional_operators], 'emotional_resonance_pattern': pattern_list}