import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings

class StableRiemannZetaOperator:
    """Numerically stable Riemann zeta function"""

    @staticmethod
    def zeta(s: complex, terms: int=100) -> complex:
        try:
            if s.real > 1:
                result = 0.0
                for n in range(1, terms):
                    term = 1.0 / n ** s
                    result += term
                    if abs(term) < 1e-15:
                        break
                return result
            else:
                pi = np.pi
                if abs(s.imag) < 1e-10 and s.real < 0 and (abs(s.real - round(s.real)) < 1e-10):
                    if round(s.real) % 2 == 0:
                        return 0.0
                if abs(s.imag) < 1e-10:
                    s += 1e-10j
                return 2 ** s * pi ** (s - 1) * np.sin(pi * s / 2) * special.gamma(1 - s) * StableRiemannZetaOperator.zeta(1 - s, terms)
        except (OverflowError, ValueError, ZeroDivisionError):
            return complex(0, 0)

    @staticmethod
    def critical_line_modulation(t: float, amplitude: float=0.001) -> complex:
        try:
            t_clipped = np.clip(t, -100, 100)
            s = 0.5 + 1j * t_clipped
            zeta_val = StableRiemannZetaOperator.zeta(s)
            return amplitude * zeta_val
        except:
            return complex(0, 0)