"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from .profile import ORCH_VENDOR as _V
if _V == "ultimate":
    from .vendor.ultimate.weighting import *  # type: ignore
else:
    from .vendor.pro.weighting import *  # type: ignore
