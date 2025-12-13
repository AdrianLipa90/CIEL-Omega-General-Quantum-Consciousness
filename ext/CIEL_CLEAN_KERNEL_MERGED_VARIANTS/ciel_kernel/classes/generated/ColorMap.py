from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

class ColorMap:
    """Mapowanie stanu rezonansu na barwy CIEL/OS."""
    palette = {'SOUL_BLUE': (0.2, 0.4, 0.9), 'INTENTION_GOLD': (0.95, 0.8, 0.2), 'ETHICS_WHITE': (1.0, 1.0, 0.95), 'WARNING_RED': (0.9, 0.2, 0.2), 'BALANCE_GREEN': (0.3, 0.9, 0.5)}

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
            return ColorMap.palette['WARNING_RED']
        elif v < 0.7:
            r1, g1, b1 = ColorMap.palette['WARNING_RED']
            r2, g2, b2 = ColorMap.palette['INTENTION_GOLD']
            f = (v - 0.3) / 0.4
            return (r1 + f * (r2 - r1), g1 + f * (g2 - g1), b1 + f * (b2 - b1))
        else:
            r1, g1, b1 = ColorMap.palette['INTENTION_GOLD']
            r2, g2, b2 = ColorMap.palette['ETHICS_WHITE']
            f = (v - 0.7) / 0.3
            return (r1 + f * (r2 - r1), g1 + f * (g2 - g1), b1 + f * (b2 - b1))