# -*- coding: utf-8 -*-
"""
CIEL/Ω – Emotional Collatz Engine (CQCL layer, self-contained)

Co jest w środku:
- CQCL_Program                 – lekki kontener programu (semantic_tree, hash, kwant.zmienne)
- CIEL_Quantum_Engine          – baza: „kompilator” intencji → program + metryki
- EmotionalCollatzEngine       – Twój silnik z operatorami emocji (love/fear/joy/anger/peace/sadness)
- Minimalny „kompilator semantyczny”:
    * wydobywa profil emocjonalny z intencji (heurystyka) + normalizacja
    * ustawia quantum_variables: resonance, superposition, quantum_flux, entanglement, coherence
- Demo: demonstracja_emocjonalnego_collatza()
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np
np.seterr(all="ignore")

# ─────────────────────────────────────────────────────────────────────────────
# Pomocnicze: sentyment, hashing, normalizacja
# ─────────────────────────────────────────────────────────────────────────────
_POS = {"love", "peace", "harmony", "cooperation", "joy", "trust", "compassion",
        "miłość", "pokój", "harmonia", "współpraca", "radość", "zaufanie", "współczucie"}
_NEG = {"fear", "anger", "war", "conflict", "hate", "despair",
        "strach", "gniew", "wojna", "konflikt", "nienawiść", "desperacja", "lęk", "smutek"}

def _stable_hash(text: str) -> int:
    # deterministyczny 64-bit hash
    return int(hashlib.blake2b(text.encode("utf-8"), digest_size=8).hexdigest(), 16)

def _sentiment(text: str) -> float:
    t = text.lower()
    p = sum(t.count(w) for w in _POS)
    n = sum(t.count(w) for w in _NEG)
    tot = p + n
    return p / tot if tot else 0.5

def _lexical_diversity(text: str) -> float:
    ws = [w for w in re.findall(r"[A-Za-zÀ-ž0-9]+", text.lower())]
    return len(set(ws)) / max(1, len(ws)) if ws else 0.0

def _normalize_profile(d: Dict[str, float]) -> Dict[str, float]:
    # obcina <0, skaluje do sumy 1 (jeśli coś jest >0)
    clipped = {k: max(0.0, float(v)) for k, v in d.items()}
    s = sum(clipped.values())
    if s <= 1e-12:
        return {k: 0.0 for k in clipped}
    return {k: v / s for k, v in clipped.items()}

# ─────────────────────────────────────────────────────────────────────────────
# CQCL – lekki model programu i bazowy engine
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class CQCL_Program:
    intent: str
    semantic_tree: Dict[str, Any]
    semantic_hash: int
    quantum_variables: Dict[str, float]
    input_data: Optional[float] = None
    computation_path: List[int] = field(default_factory=list)
    execution_trace: List[Dict[str, Any]] = field(default_factory=list)

class CIEL_Quantum_Engine:
    """Baza: kompilacja intencji → CQCL_Program oraz liczenie metryk bazowych."""
    def __init__(self) -> None:
        self.compiler = self  # prosto: ta sama klasa pełni rolę kompilatora

    # ---- „kompilator” intencji → program CQCL ----
    def compile_program(self, intention: str, input_data: Any = None) -> CQCL_Program:
        emo_profile = self._build_emotional_profile(intention)
        qvars = self._build_quantum_variables(intention, emo_profile)
        sem_hash = _stable_hash(intention)
        return CQCL_Program(
            intent=intention,
            semantic_tree={"emotional_profile": emo_profile},
            semantic_hash=sem_hash,
            quantum_variables=qvars,
            input_data=float(input_data) if input_data is not None else None,
        )

    def _build_emotional_profile(self, intention: str) -> Dict[str, float]:
        # heurystyka: mapuje słowa kluczowe → emocje; gdy brak, rozkład neutralny
        t = intention.lower()
        prof = {
            "love": 0.15 + 0.25 * sum(t.count(w) for w in {"love", "miłość", "compassion"}) ,
            "joy":  0.10 + 0.20 * sum(t.count(w) for w in {"joy", "radość", "entuzjazm"}),
            "peace":0.10 + 0.20 * sum(t.count(w) for w in {"peace", "pokój", "harmonia"}),
            "fear": 0.05 + 0.20 * sum(t.count(w) for w in {"fear", "strach", "lęk"}),
            "anger":0.05 + 0.20 * sum(t.count(w) for w in {"anger", "gniew"}),
            "sadness":0.05+0.20 * sum(t.count(w) for w in {"sadness","smutek"}),
        }
        # drobna modyfikacja globalna wg sentymentu
        s = _sentiment(intention)
        prof["love"] += 0.1 * s
        prof["joy"]  += 0.05 * s
        prof["fear"] += 0.05 * (1 - s)
        prof["anger"]+= 0.03 * (1 - s)
        return _normalize_profile(prof)

    def _build_quantum_variables(self, intention: str, emo: Dict[str, float]) -> Dict[str, float]:
        # wartości w [0,1], deterministyczne; zależne od emocji i różnorodności leksykalnej
        diversity = _lexical_diversity(intention)
        return {
            "resonance":     0.2 + 0.6 * (emo.get("peace", 0)+emo.get("love",0)),           # „zgodność”
            "superposition": 0.3 + 0.6 * diversity,                                         # złożoność treści
            "quantum_flux":  0.2 + 0.6 * (emo.get("joy",0) + emo.get("anger",0)*0.5),       # ruchliwość
            "entanglement":  0.3 + 0.5 * (sum(emo.values())/6.0),                            # „spięcie emocji”
            "coherence":     0.4 + 0.5 * (emo.get("love",0) + emo.get("peace",0) - emo.get("fear",0)/2),
        }

    # ---- metryki bazowe (wykorzystywane w emocjonalnych metrykach) ----
    def _calculate_comprehensive_metrics(self, program: CQCL_Program,
                                         computation_result: Dict[str, Any],
                                         final_result: complex) -> Dict[str, float]:
        q = program.quantum_variables
        return {
            "quantum_coherence": float(np.clip(q.get("coherence", 0.0), 0.0, 1.0)),
            "quantum_flux": float(np.clip(q.get("quantum_flux", 0.0), 0.0, 1.0)),
            "entanglement": float(np.clip(q.get("entanglement", 0.0), 0.0, 1.0)),
        }

# ─────────────────────────────────────────────────────────────────────────────
# Emotional Collatz – Twój silnik, dopięty do bazy
# ─────────────────────────────────────────────────────────────────────────────
class EmotionalCollatzEngine(CIEL_Quantum_Engine):
    """Silnik CQCL z rozszerzoną komputacją emocjonalną Collatza."""
    def __init__(self):
        super().__init__()
        self.emotional_operators = self._initialize_emotional_operators()

    def _initialize_emotional_operators(self) -> Dict[str, Dict[str, Any]]:
        return {
            'love': {
                'function': lambda n, intensity: n * (1 + intensity) if n % 2 == 0 else 3*n + int(10*intensity),
                'description': 'Mnożenie przez miłość - ekspansja harmoniczna'
            },
            'fear': {
                'function': lambda n, intensity: max(1, int(n // max(1.0, (2 + intensity)))) if n % 2 == 0 else max(1, n - int(5*intensity)),
                'description': 'Redukcja przez strach - kontrakcja ochronna'
            },
            'joy': {
                'function': lambda n, intensity: int(n // 2 + int(10*intensity)) if n % 2 == 0 else 3*n + int(20*intensity),
                'description': 'Eksplozja radości - wzmocniona kreatywność'
            },
            'anger': {
                'function': lambda n, intensity: int(n * (2 + intensity)) if n % 2 == 0 else 5*n + int(15*intensity),
                'description': 'Mnożenie gniewu - intensyfikacja transformacji'
            },
            'peace': {
                'function': lambda n, intensity: max(1, int(n // max(1.0, (1 + intensity)))) if n % 2 == 0 else n + 1,
                'description': 'Wyciszenie pokoju - łagodna konwergencja'
            },
            'sadness': {
                'function': lambda n, intensity: max(1, n - int(3*intensity)) if n % 2 == 0 else max(1, int(n // 2)),
                'description': 'Redukcja smutku - spowolniona ewolucja'
            }
        }

    # ——— Collatz modyfikowany emocjami ———
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
            # domyślny Collatz
            return n // 2 if n % 2 == 0 else 3*n + 1
        return max(1, int(emotional_mix / total_w))

    # ——— Główna ścieżka uruchomienia programu ———
    def execute_emotional_program(self, intention: str, input_data: Any = None) -> Dict[str, Any]:
        program = self.compiler.compile_program(intention, input_data)
        emotional_path = self._generate_emotional_collatz_path(program)
        program.computation_path = emotional_path
        computation_result = self._execute_emotional_computation(program)
        final_result = self._apply_emotional_ramanujan_resonance(computation_result, program)
        metrics = self._calculate_emotional_metrics(program, computation_result, final_result)
        return {
            'program': program,
            'computation_result': computation_result,
            'final_result': final_result,
            'metrics': metrics,
            'emotional_landscape': self._analyze_emotional_landscape(program, emotional_path)
        }

    def _generate_emotional_collatz_path(self, program: CQCL_Program) -> List[int]:
        emotional_profile = dict(program.semantic_tree['emotional_profile'])
        seed = program.semantic_hash % 10000 + 1
        current, path, max_iterations = seed, [], 300
        iter_no = 0
        while current != 1 and iter_no < max_iterations:
            path.append(current)
            current = self.emotional_collatz_transform(current, emotional_profile)
            # lekkie „życie” profilu co 10 kroków
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
        interm, emo_amps, coh_hist = [], [], []
        current_state = complex(program.input_data or 1.0, 0.0)

        # stałe (zabezpieczenie zakresów)
        resonance = float(np.clip(qv['resonance'], 0.0, 1.0))
        superpos  = float(np.clip(qv['superposition'], 0.0, 1.0))
        qflux     = float(np.clip(qv['quantum_flux'], 0.0, 1.0))
        ent       = float(np.clip(qv['entanglement'], 0.0, 1.0))
        base_coh  = float(np.clip(qv['coherence'], 0.0, 1.0))

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
                # „splątanie emocji”: suma fazowanych składowych
                entang = 0j
                for emotion, intensity in emo_prof.items():
                    ph = ((hashlib.sha1(emotion.encode()).digest()[0]) % 100) / 100.0 * math.pi
                    entang += intensity * np.exp(1j * ph)
                current_state += entang * ent * 0.1

            interm.append(current_state)
            emo_amps.append(abs(current_state) * (1 + emo_intensity))
            coh_hist.append(base_coh * ((0.9 + 0.1 * emo_intensity) ** step))

            program.execution_trace.append({
                'step': step, 'collatz_number': cn, 'state': current_state,
                'amplitude': abs(current_state), 'emotional_intensity': emo_intensity,
                'emotional_profile': dict(emo_prof)
            })

        return {
            'final_state': current_state,
            'intermediate_states': interm,
            'emotional_amplitudes': emo_amps,
            'coherence_history': coh_hist,
            'path_length': len(path),
            'max_emotional_amplitude': max(emo_amps) if emo_amps else 0.0,
            'emotional_convergence': self._calculate_emotional_convergence(emo_amps)
        }

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
            h = (hashlib.blake2b(emotion.encode(), digest_size=2).digest()[0]) / 255.0
            corr *= (1.0 + intensity * h * 0.1)
        emo_phase = sum(intensity * ((hashlib.sha1(em.encode()).digest()[0]) % 100) / 100.0
                        for em, intensity in emo.items())
        phase = np.exp(1j * 2 * np.pi * (emo_phase / max(1, len(emo))))
        return raw * corr * phase

    def _calculate_emotional_metrics(self, program: CQCL_Program,
                                     computation_result: Dict[str, Any],
                                     final_result: complex) -> Dict[str, float]:
        base = super()._calculate_comprehensive_metrics(program, computation_result, final_result)
        emo = program.semantic_tree['emotional_profile']
        emo_vals = list(emo.values())
        emotional_balance = 1.0 - abs(emo.get('love',0) - emo.get('fear',0))
        emotional_diversity = len([v for v in emo_vals if v > 0.1]) / max(1, len(emo_vals))
        emotional_intensity = sum(emo_vals) / max(1, len(emo_vals))
        emotional_coherence = float(computation_result['emotional_convergence'])
        base.update({
            'emotional_coherence': emotional_coherence,
            'emotional_intensity': emotional_intensity,
            'emotional_diversity': emotional_diversity,
            'emotional_balance': emotional_balance,
            'heart_mind_coherence': base['quantum_coherence'] * emotional_coherence
        })
        return base

    def _analyze_emotional_landscape(self, program: CQCL_Program, path: List[int]) -> Dict[str, Any]:
        emo = program.semantic_tree['emotional_profile']
        dominant = max(emo.items(), key=lambda x: x[1])[0] if emo else "none"
        changes = np.diff(path) if len(path) > 1 else np.array([])
        if len(changes) > 0:
            growth = int(np.sum(changes > 0))
            decay  = int(np.sum(changes < 0))
            if growth > 2 * decay: pat = "EKSPANSJA_EMOCJONALNA"
            elif decay > 2 * growth: pat = "KONTRAKCJA_EMOCJONALNA"
            else: pat = "RÓWNOWAGA_EMOCJONALNA"
        else:
            pat = "BRAK_WZORCA"
        peaks = 0
        if len(path) > 2:
            for i in range(1, len(path)-1):
                if path[i-1] < path[i] > path[i+1]:
                    peaks += 1
        if peaks > len(path)//10:
            pattern_list = [pat, "CYKLICZNOŚĆ_EMOCJONALNA"]
        else:
            pattern_list = [pat]
        return {
            'dominant_emotion': dominant,
            'emotional_complexity': len([v for v in emo.values() if v > 0.2]),
            'path_emotional_signature': int(_stable_hash(str(tuple(path))) % 10000),
            'emotional_operators_used': [e for e, v in emo.items() if v > 0.3 and e in self.emotional_operators],
            'emotional_resonance_pattern': pattern_list,
        }

# ─────────────────────────────────────────────────────────────────────────────
# DEMO (możesz wywołać ręcznie)
# ─────────────────────────────────────────────────────────────────────────────
def demonstracja_emocjonalnego_collatza():
    print("🎭 EMOCJONALNY COLLATZ – DEMO")
    engine = EmotionalCollatzEngine()
    testowe_intencje = [
        "Kocham życie i wszystko co ze sobą niesie – pełen entuzjazmu i radości",
        "Obawiam się przyszłości, ale pragnę znaleźć w sobie siłę i odwagę",
        "Jestem zły na niesprawiedliwość świata, ale chcę to zmienić przez działanie",
        "Czuję głęboki spokój i jedność z wszechświatem – wszystko jest idealne",
        "Smutek miesza się z nadzieją w poszukiwaniu sensu istnienia"
    ]
    for i, intencja in enumerate(testowe_intencje, 1):
        print(f"\n🧠 TEST {i}: {intencja[:72]}…")
        out = engine.execute_emotional_program(intencja, input_data=42)
        final = out['final_result']
        metrics = out['metrics']
        land = out['emotional_landscape']
        print(f"   📊 final_result ≈ {final.real:+.4e} + {final.imag:+.4e}j")
        print(f"   📈 emotional_coherence={metrics['emotional_coherence']:.4f} | "
              f"heart_mind_coherence={metrics['heart_mind_coherence']:.4f}")
        print(f"   🎭 dominant={land['dominant_emotion']} | patterns={', '.join(land['emotional_resonance_pattern'])}")

if __name__ == "__main__":
    demonstracja_emocjonalnego_collatza()