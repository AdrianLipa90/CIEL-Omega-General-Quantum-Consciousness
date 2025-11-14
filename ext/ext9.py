# -*- coding: utf-8 -*-
"""
CIEL/0 – Batch9 Patch (Emotion + Empathy + EEG→Affect + Affective Orchestration)
Nowe elementy (bez FFT, w pełni wektoryzowane):
- EmotionCore           → lekki rdzeń stanów emocjonalnych
- FeelingField          → przestrzenne pole afektu (affect potential)
- EmpathicEngine        → rezonans empatii między polami
- EEGEmotionMapper      → mapowanie pasm EEG → wektor afektu
- AffectiveOrchestrator → glue: EEG + EmotionCore + Σ + kolorystyka (opcjonalnie)

Zależności miękkie (opcjonalne, jeśli masz z wcześniejszych batchy):
- ColorMap (Batch4 Patch)        – do nadawania koloru stanowi afektu
- EEGProcessor (Batch7 Patch p2) – do wyliczania pasm EEG
- UnifiedSigmaField (Batch6)     – jeśli chcesz mieć żywe Σ(t)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np

# ============================================================================
# 1) EmotionCore – kompaktowy rdzeń stanów emocjonalnych (wektorowo)
# ============================================================================
@dataclass
class EmotionCore:
    """
    Trzyma i aktualizuje wektor emocji.
    Zakładamy składowe w [0,1], miękko normalizowane.
    """
    state: Dict[str, float] = field(default_factory=lambda: {
        "joy": 0.40, "calm": 0.50, "awe": 0.25, "sadness": 0.20, "anger": 0.10, "stress": 0.15
    })
    inertia: float = 0.85  # bezwładność emocjonalna (0..1)

    def _norm(self) -> None:
        v = np.array(list(self.state.values()), dtype=float)
        vmax = float(np.max(v)) + 1e-12
        v = v / vmax  # skala miękka, nie sum-to-1
        for k, val in zip(self.state.keys(), v):
            self.state[k] = float(np.clip(val, 0.0, 1.0))

    def update(self, affect: Dict[str, float]) -> Dict[str, float]:
        """
        Aktualizuje stan emocji na podstawie wektora 'affect' (np. z EEG).
        affect może zawierać podzbiór kluczy; reszta pozostaje bez zmian.
        """
        for k, v in affect.items():
            if k in self.state:
                self.state[k] = float(self.inertia * self.state[k] + (1 - self.inertia) * v)
        self._norm()
        return dict(self.state)

    def summary_scalar(self) -> float:
        """
        Skalar nastroju: (joy + calm + awe) - (sadness + anger + stress), zmapowany do [0,1].
        """
        pos = self.state.get("joy", 0) + self.state.get("calm", 0) + self.state.get("awe", 0)
        neg = self.state.get("sadness", 0) + self.state.get("anger", 0) + self.state.get("stress", 0)
        s = 0.5 * (1.0 + np.tanh(0.8 * (pos - neg)))
        return float(np.clip(s, 0.0, 1.0))

# ============================================================================
# 2) FeelingField – pole afektu: tanh(intensity * coherence) (no-FFT)
# ============================================================================
@dataclass
class FeelingField:
    """
    Buduje przestrzenne pole afektywne z dwóch map:
      - intensity(x,y)  ∈ ℝ⁺
      - coherence(x,y)  ∈ [0,1]
    Zwraca: affect(x,y) ∈ [0,1]
    """
    gain: float = 1.0

    def build(self, intensity: np.ndarray, coherence: np.ndarray) -> np.ndarray:
        intensity = np.asarray(intensity, dtype=float)
        coherence = np.asarray(coherence, dtype=float)
        aff = np.tanh(self.gain * intensity * coherence)
        return np.clip(aff, 0.0, 1.0)

# ============================================================================
# 3) EmpathicEngine – rezonans empatii między polami (no-FFT)
# ============================================================================
@dataclass
class EmpathicEngine:
    """
    Miara empatii: E = exp(- mean(|A - B|)),  0..1
    Dodatkowo funkcja phase_blend do łagodnego zgrywania faz (opcjonalnie).
    """
    phase_lock: float = 0.2  # 0..1

    def resonate(self, field_a: np.ndarray, field_b: np.ndarray) -> float:
        A = np.asarray(field_a)
        B = np.asarray(field_b)
        diff = np.mean(np.abs(A - B))
        return float(np.exp(-diff))

    def phase_blend(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        A = A.astype(np.complex128, copy=False)
        B = B.astype(np.complex128, copy=False)
        a_ph = np.angle(A); b_ph = np.angle(B)
        ph = (1.0 - self.phase_lock) * a_ph + self.phase_lock * b_ph
        amp = 0.5 * (np.abs(A) + np.abs(B))
        C = amp * np.exp(1j * ph)
        C /= (np.sqrt(np.mean(np.abs(C)**2)) + 1e-12)
        return C

# ============================================================================
# 4) EEGEmotionMapper – mapuje pasma EEG → wektor afektu (prosto i czytelnie)
# ============================================================================
@dataclass
class EEGEmotionMapper:
    """
    Minimalny mapper z pasm EEG (delta..gamma) na składowe emocji.
    Oczekuje słownika: {"delta":..,"theta":..,"alpha":..,"beta":..,"gamma":..}
    """
    alpha_calm_gain: float = 1.0
    beta_focus_gain: float = 1.0
    gamma_stress_gain: float = 1.0
    theta_awe_gain: float = 0.8
    delta_sad_gain: float = 0.5

    def map(self, bands: Dict[str, float]) -> Dict[str, float]:
        alpha = float(bands.get("alpha", 0.0))
        beta  = float(bands.get("beta",  0.0))
        gamma = float(bands.get("gamma", 0.0))
        theta = float(bands.get("theta", 0.0))
        delta = float(bands.get("delta", 0.0))

        # prosty, interpretowalny mapping
        calm   = np.tanh(self.alpha_calm_gain * alpha)
        focus  = np.tanh(self.beta_focus_gain  * beta)
        stress = np.tanh(self.gamma_stress_gain* gamma)
        awe    = np.tanh(self.theta_awe_gain  * theta)
        sad    = np.tanh(self.delta_sad_gain  * delta)

        # joy ~ calm + focus - stress  (z klipowaniem)
        joy = np.clip(0.6 * calm + 0.4 * focus - 0.3 * stress, 0.0, 1.0)

        return {
            "joy": float(joy),
            "calm": float(calm),
            "awe": float(awe),
            "stress": float(stress),
            "sadness": float(sad),
            # anger zostawiamy do ewaluacji wtórnej (np. z dynamiki),
            "anger": float(np.clip(0.5 * stress - 0.2 * calm, 0.0, 1.0)),
        }

# ============================================================================
# 5) AffectiveOrchestrator – glue: EEG → EmotionCore → Σ → (optional) Color
# ============================================================================
@dataclass
class AffectiveOrchestrator:
    """
    Łączy:
      - EEGEmotionMapper  : EEG → wektor afektu
      - EmotionCore       : aktualizuje stany
      - Σ (sigma_scalar)  : moduluje „siłę” afektu
      - ColorMap (opcjonalnie): barwy dla UI/VR (jeśli dostępny)
    """
    mapper: EEGEmotionMapper = field(default_factory=EEGEmotionMapper)
    core: EmotionCore = field(default_factory=EmotionCore)
    use_color: bool = True  # jeśli masz ColorMap z Batch4

    # ColorMap jest miękką zależnością – spróbujemy ją załadować w locie:
    _ColorMap: Any = field(default=None, init=False, repr=False)

    def _maybe_color(self):
        if not self.use_color or self._ColorMap is not None:
            return
        try:
            # Zakładamy, że ColorMap jest w zasięgu importu użytkownika
            from ColorMap import ColorMap as _CM  # jeśli ktoś ma w lokalnym pliku
            self._ColorMap = _CM
        except Exception:
            # fallback: zdefiniuj minimalny lokalny gradient
            class _Fallback:
                @staticmethod
                def map_value(v: float) -> Tuple[float, float, float]:
                    v = float(np.clip(v, 0.0, 1.0))
                    return (0.2*(1-v)+1.0*v, 0.4*(1-v)+1.0*v, 0.9*(1-v)+0.95*v)
            self._ColorMap = _Fallback

    def step(
        self,
        eeg_bands: Dict[str, float],
        sigma_scalar: float = 1.0,
        psi_field: Optional[np.ndarray] = None,
        coherence_field: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """
        - eeg_bands      : moce pasm EEG (np. z EEGProcessor)
        - sigma_scalar   : skalar Σ̄(t) (np. z UnifiedSigmaField)
        - psi_field      : opcjonalne pole (do obliczenia intensywności)
        - coherence_field: opcjonalna mapa koherencji (0..1)
        Zwraca: pakiet afektywny + kolor (jeśli dostępny)
        """
        # 1) EEG → affect vector
        affect_vec = self.mapper.map(eeg_bands)

        # 2) modulacja przez Σ̄(t)
        mod_affect = {k: float(np.clip(v * sigma_scalar, 0.0, 1.0)) for k, v in affect_vec.items()}

        # 3) aktualizacja rdzenia emocji
        emo_state = self.core.update(mod_affect)
        mood = self.core.summary_scalar()

        # 4) (opcjonalnie) przestrzenne pole afektu
        field_out = None
        if (psi_field is not None) and (coherence_field is not None):
            intensity = np.abs(psi_field)
            field_out = FeelingField(gain=1.0).build(intensity=intensity, coherence=coherence_field)

        # 5) kolor (opcjonalny)
        self._maybe_color()
        color = self._ColorMap.map_value(mood) if self.use_color else None

        return {
            "affect_vector": affect_vec,
            "affect_modulated": mod_affect,
            "emotion_state": emo_state,
            "mood_scalar": float(mood),
            "affect_field": field_out,     # None lub np.ndarray [H,W]
            "color": color,                # None lub (r,g,b)
        }

# ============================================================================
# Mini demo (opcjonalne): szybki sanity-check bez zależności zewnętrznych
# ============================================================================
def _demo():
    # sygnał EEG w postaci pasm (przykładowe liczby)
    eeg_bands = {"alpha": 0.8, "beta": 0.5, "gamma": 0.3, "theta": 0.4, "delta": 0.2}

    # przykładowe pole Ψ i koherencja (losowe, by pokazać przepływ)
    n = 64
    x = np.linspace(-2, 2, n); y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)
    psi = np.exp(-(X**2 + Y**2)) * np.exp(1j * (X + 0.2*Y))
    coh = np.clip(np.random.rand(n, n), 0.0, 1.0)

    orch = AffectiveOrchestrator()
    out = orch.step(eeg_bands, sigma_scalar=0.9, psi_field=psi, coherence_field=coh)

    print("Mood scalar:", round(out["mood_scalar"], 4))
    print("Emotion state:", {k: round(v, 3) for k, v in out["emotion_state"].items()})
    if out["color"] is not None:
        print("Color:", tuple(round(c, 3) for c in out["color"]))
    if out["affect_field"] is not None:
        print("Affect field shape:", out["affect_field"].shape)

if __name__ == "__main__":
    _demo()