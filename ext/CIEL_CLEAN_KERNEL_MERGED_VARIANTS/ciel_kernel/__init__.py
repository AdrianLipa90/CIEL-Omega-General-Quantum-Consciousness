"""CIEL/Ω — clean kernel.

Zawiera:
- zunifikowane stałe fizyczne i matematyczne,
- parametry strojenia modeli,
- lekki orkiestrator sterujący modułami CIEL.
"""

from .constants import PhysicalConstants, MathematicalConstants, ModelTuningParameters
from .orchestrator import CIELKernel, CIELModule
