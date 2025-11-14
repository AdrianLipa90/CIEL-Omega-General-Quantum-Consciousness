# -*- coding: utf-8 -*-
"""
CIEL/0 – Batch10 Patch (Cognitive Loop: Perception → Intuition → Prediction → Decision)
Nowe elementy, bez duplikatów i bez FFT:
- PerceptiveLayer      → sensoryczna mapa pól: Percept = Σ * (Re(Ψ) + |Im(Ψ)|)
- IntuitiveCortex      → intuicyjna synteza wejść (entropijne ważenie)
- PredictiveCore       → nieliniowa predykcja (ważona pamięć, bez uczenia)
- DecisionCore         → wybór akcji: score = intent * ethic * confidence
- CognitionOrchestrator→ pętla poznawcza z hookami (pre/post), logi kroków

Kompatybilne z wcześniejszymi patchami (Σ, ColorMap, EEG, Ethics), ale od nich niezależne.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# 1) PerceptiveLayer – mapa percepcyjna Ψ × Σ
#    Percept(x,y) = Σ_field(x,y) * ( Re(Ψ) + |Im(Ψ)| )
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PerceptiveLayer:
    clip_percentile: Optional[float] = 99.5  # przytnij skrajności (opcjonalnie)

    def compute(self, psi_field: np.ndarray, sigma_field: np.ndarray) -> np.ndarray:
        psi = psi_field.astype(np.complex128, copy=False)
        sig = sigma_field.astype(np.float64, copy=False)
        percept = sig * (psi.real + np.abs(psi.imag))
        if self.clip_percentile is not None:
            hi = np.percentile(percept, self.clip_percentile)
            percept = np.clip(percept, 0.0, hi) / (hi + 1e-12)
        else:
            percept = percept / (np.max(percept) + 1e-12)
        return percept

# ─────────────────────────────────────────────────────────────────────────────
# 2) IntuitiveCortex – entropijna intuicja (wektorowo, bez uczenia)
#    intuition(inputs): tanh( dot( exp(-entropy_map), inputs ) )
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class IntuitiveCortex:
    """Lekka synteza „przeczucia” na podstawie mapy entropii i bufora pamięci."""
    entropy_map: np.ndarray  # 1D lub 2D (spłaszczane)
    predictivity: float = 0.7
    memory_buffer: List[np.ndarray] = field(default_factory=list)
    max_memory: int = 64

    def _weights(self) -> np.ndarray:
        w = np.exp(-np.asarray(self.entropy_map, dtype=float).ravel())
        return w / (np.sum(w) + 1e-12)

    def ingest(self, obs: np.ndarray) -> None:
        v = np.asarray(obs, dtype=float).ravel()
        self.memory_buffer.append(v)
        if len(self.memory_buffer) > self.max_memory:
            self.memory_buffer.pop(0)

    def intuition(self, inputs: np.ndarray) -> float:
        x = np.asarray(inputs, dtype=float).ravel()
        w = self._weights()
        raw = np.dot(w, x)
        # domieszka „pamięci” (średnia z bufora)
        if self.memory_buffer:
            m = np.mean(np.stack(self.memory_buffer, axis=0), axis=0)
            raw = (1 - self.predictivity) * raw + self.predictivity * float(np.dot(w, m))
        return float(np.tanh(raw))

    def update_entropy(self, percept: np.ndarray, k: float = 0.1) -> None:
        """Prosta adaptacja entropii: spadek dla wzorców częstych, wzrost dla rzadkich."""
        p = np.asarray(percept, dtype=float).ravel()
        p = p / (np.max(p) + 1e-12)
        # im większy sygnał, tym niższa entropia (łatwo rozpoznawalne)
        self.entropy_map = np.clip(self.entropy_map - k * p + 0.5 * k * (1 - p), 0.0, 5.0)

# ─────────────────────────────────────────────────────────────────────────────
# 3) PredictiveCore – beznadzorowa predykcja (ważona przeszłość)
#    predict(history): sum( exp(-t/τ) * x_t ) / sum( exp(-t/τ) )
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PredictiveCore:
    tau: float = 12.0  # stała zaniku pamięci

    def predict(self, history: List[float]) -> float:
        if not history:
            return 0.0
        h = np.asarray(history, dtype=float)
        t = np.arange(len(h))[::-1]  # 0 = najświeższe
        w = np.exp(-t / max(self.tau, 1e-6))
        return float(np.sum(w * h) / (np.sum(w) + 1e-12))

# ─────────────────────────────────────────────────────────────────────────────
# 4) DecisionCore – wybór akcji z etyką i pewnością
#    score = intent * ethic * confidence
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class DecisionCore:
    min_score: float = 0.15  # minimalny akceptowalny wynik

    def decide(self, options: Dict[str, Dict[str, float]]) -> Tuple[Optional[str], Dict[str, float]]:
        """
        options = {
          "action_name": {"intent":0..1, "ethic":0..1, "confidence":0..1},
          ...
        }
        Zwraca (najlepsza_akcja_lub_None, słownik_score_ów).
        """
        scores = {}
        best_key, best_val = None, -np.inf
        for k, v in options.items():
            s = float(v.get("intent", 0.0) * v.get("ethic", 0.0) * v.get("confidence", 0.0))
            scores[k] = s
            if s > best_val:
                best_key, best_val = k, s
        if best_val < self.min_score:
            return None, scores
        return best_key, scores

# ─────────────────────────────────────────────────────────────────────────────
# 5) CognitionOrchestrator – pętla poznawcza
#    Perception → Intuition → Prediction → Decision (hooki pre/post)
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class CognitionOrchestrator:
    percept: PerceptiveLayer
    cortex: IntuitiveCortex
    predictor: PredictiveCore
    decider: DecisionCore
    pre_step: Optional[Callable[[int, Dict[str, Any]], None]] = None
    post_step: Optional[Callable[[int, Dict[str, Any]], None]] = None

    # pamięć stanu
    _intuition_hist: List[float] = field(default_factory=list, init=False)
    _log: List[Dict[str, Any]] = field(default_factory=list, init=False)

    def run_cycle(
        self,
        steps: int,
        psi_supplier: Callable[[int], np.ndarray],
        sigma_supplier: Callable[[int], np.ndarray],
        options_supplier: Callable[[int, float, float], Dict[str, Dict[str, float]]],
    ) -> List[Dict[str, Any]]:
        """
        psi_supplier(t)   → pole Ψ (H×W) w kroku t
        sigma_supplier(t) → pole Σ (H×W) w kroku t
        options_supplier(t, intuition, prediction) → kandydaci decyzji
        Zwraca listę logów ze wszystkich kroków.
        """
        self._intuition_hist.clear()
        self._log.clear()

        for t in range(steps):
            ctx: Dict[str, Any] = {"t": t}

            if self.pre_step:
                self.pre_step(t, ctx)

            # 1) Perception
            psi = psi_supplier(t)
            sigma = sigma_supplier(t)
            percept = self.percept.compute(psi, sigma)
            ctx["percept_mean"] = float(np.mean(percept))

            # 2) Intuition (z adaptacją entropii)
            self.cortex.ingest(percept)
            intuition = self.cortex.intuition(percept)
            self.cortex.update_entropy(percept, k=0.05)
            self._intuition_hist.append(intuition)
            ctx["intuition"] = float(intuition)

            # 3) Prediction
            pred = self.predictor.predict(self._intuition_hist)
            ctx["prediction"] = float(pred)

            # 4) Decision
            options = options_supplier(t, intuition, pred)
            choice, scores = self.decider.decide(options)
            ctx["decision"] = choice
            ctx["scores"] = scores

            if self.post_step:
                self.post_step(t, ctx)

            self._log.append(ctx)

        return list(self._log)

# ─────────────────────────────────────────────────────────────────────────────
# Mini-demo: krótki sanity check (samowystarczalny)
# ─────────────────────────────────────────────────────────────────────────────
def _demo():
    # sztuczne pola Ψ i Σ
    n = 64
    x = np.linspace(-2, 2, n); y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi0 = np.exp(-(X**2 + Y**2)) * np.exp(1j * (X + 0.3 * Y))
    sigma0 = np.exp(-(X**2 + Y**2) / 2.0)

    # dostawcy
    def psi_supplier(t: int):
        return psi0 * np.exp(1j * 0.05 * t)

    def sigma_supplier(t: int):
        return np.clip(sigma0 * (0.95 + 0.05 * np.cos(0.1 * t)), 0.0, 1.0)

    def options_supplier(t: int, intuition: float, prediction: float):
        # przykładowe trzy działania: help / wait / risky
        base_ethic = 0.9
        return {
            "help":  {"intent": max(0.0, intuition),           "ethic": base_ethic,     "confidence": 0.7 + 0.2*prediction},
            "wait":  {"intent": 0.4 + 0.3*(1 - abs(intuition)),"ethic": 0.8,            "confidence": 0.6},
            "risky": {"intent": 0.6*prediction,                 "ethic": 0.4 + 0.2*t%2, "confidence": 0.5},
        }

    # instancje
    percept = PerceptiveLayer()
    cortex  = IntuitiveCortex(entropy_map=np.ones(n*n))
    pred    = PredictiveCore(tau=10.0)
    decide  = DecisionCore(min_score=0.2)
    cog     = CognitionOrchestrator(percept, cortex, pred, decide)

    logs = cog.run_cycle(steps=12, psi_supplier=psi_supplier, sigma_supplier=sigma_supplier, options_supplier=options_supplier)
    # zwięzłe podsumowanie
    print("Last 3 steps:")
    for row in logs[-3:]:
        print(f"t={row['t']:02d}  intu={row['intuition']:.3f}  pred={row['prediction']:.3f}  choice={row['decision']}")

if __name__ == "__main__":
    _demo()