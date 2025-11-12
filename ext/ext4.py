# -*- coding: utf-8 -*-
"""
CIEL/0 – Batch4 Patch (Ethical Engine + Decay + Color Mapper)
Uzupełnienie do wcześniejszych modułów:
dodaje brakujące klasy etyczne, mechanizm tłumienia energii moralnej
i prosty system kolorów CIEL/OS do wizualizacji rezonansu.

Nie zawiera duplikatów z batch2/batch3.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

# ==============================================================
# 1️⃣ Główny silnik etyki – wyciąg z ETHICAL FULL CORE
# ==============================================================
@dataclass
class EthicalEngine:
    """Dynamiczna ocena etyczna w oparciu o spójność, intencję i masę."""
    bound: float = 0.9
    history: list = field(default_factory=list)

    def evaluate(self, coherence: float, intention: float, mass: float) -> float:
        """Zwraca wartość etyczną (0–1)."""
        score = (coherence * intention) / (mass + 1e-12)
        value = np.tanh(score / self.bound)
        self.history.append(float(value))
        return float(value)

    def mean_score(self) -> float:
        return float(np.mean(self.history)) if self.history else 0.0

# ==============================================================
# 2️⃣ Lekki strażnik – z class EthicalCore.txt
# ==============================================================
class EthicalCoreLite:
    """Minimalny strażnik etyki – szybka kontrola spójności."""
    ETHICAL_BOUND = 0.9
    HARMONIC_TOL = 0.05

    @staticmethod
    def check(coherence: float, resonance: float) -> bool:
        """Zwraca True, jeśli system zachowuje równowagę etyczną."""
        return (coherence * resonance) > (EthicalCoreLite.ETHICAL_BOUND - EthicalCoreLite.HARMONIC_TOL)

# ==============================================================
# 3️⃣ Tłumik etyczny – CIEL_ET.txt
# ==============================================================
def ethical_decay(E: float, tau: float = 0.05) -> float:
    """Redukcja 'napięcia etycznego' – model relaksacji energii moralnej."""
    return float(np.exp(-E * tau))

def energy_to_time(E: float, h: float = 6.62607015e-34) -> float:
    """Konwersja energii do czasu w wymiarze etycznym."""
    return h / (E + 1e-12)

# ==============================================================
# 4️⃣ Kolorystyka CIEL/OS – ColorOS.txt
# ==============================================================
class ColorMap:
    """Mapowanie stanu rezonansu na barwy CIEL/OS."""
    palette = {
        "SOUL_BLUE": (0.2, 0.4, 0.9),
        "INTENTION_GOLD": (0.95, 0.8, 0.2),
        "ETHICS_WHITE": (1.0, 1.0, 0.95),
        "WARNING_RED": (0.9, 0.2, 0.2),
        "BALANCE_GREEN": (0.3, 0.9, 0.5)
    }

    @staticmethod
    def map_value(v: float) -> tuple[float, float, float]:
        """
        Zwraca kolor RGB dla danej wartości rezonansu/etyki (0–1).
        - 0 → czerwony (ostrzeżenie)
        - 0.5 → złoty
        - 1 → biały (pełna harmonia)
        """
        v = max(0.0, min(1.0, v))
        if v < 0.3:
            return ColorMap.palette["WARNING_RED"]
        elif v < 0.7:
            # gradient od czerwonego do złotego
            r1, g1, b1 = ColorMap.palette["WARNING_RED"]
            r2, g2, b2 = ColorMap.palette["INTENTION_GOLD"]
            f = (v - 0.3) / 0.4
            return (r1 + f*(r2-r1), g1 + f*(g2-g1), b1 + f*(b2-b1))
        else:
            # gradient od złotego do białego
            r1, g1, b1 = ColorMap.palette["INTENTION_GOLD"]
            r2, g2, b2 = ColorMap.palette["ETHICS_WHITE"]
            f = (v - 0.7) / 0.3
            return (r1 + f*(r2-r1), g1 + f*(g2-g1), b1 + f*(b2-b1))

# ==============================================================
# 5️⃣ Mini integrator do testu etycznego (opcjonalny)
# ==============================================================
@dataclass
class EthicalMonitor:
    """Łączy silnik, strażnika i kolory w prosty model obserwacyjny."""
    engine: EthicalEngine = field(default_factory=EthicalEngine)
    lite: EthicalCoreLite = field(default_factory=EthicalCoreLite)

    def evaluate_and_color(self, coherence: float, intention: float, mass: float) -> tuple[float, tuple[float, float, float]]:
        """Ocena i wizualizacja stanu etycznego."""
        value = self.engine.evaluate(coherence, intention, mass)
        ok = self.lite.check(coherence, value)
        color = ColorMap.map_value(value if ok else value * 0.5)
        return value, color

# ==============================================================
# 6️⃣ Demo
# ==============================================================
def _demo():
    monitor = EthicalMonitor()
    for c in np.linspace(0.1, 1.0, 6):
        val, col = monitor.evaluate_and_color(c, intention=0.8, mass=0.5)
        print(f"coh={c:.2f} → ethics={val:.3f}, color={col}, decay={ethical_decay(val):.3f}")

if __name__ == "__main__":
    _demo()