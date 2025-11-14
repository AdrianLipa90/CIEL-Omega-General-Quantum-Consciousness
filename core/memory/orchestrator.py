"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from .profile import ORCH_VENDOR as _V
if _V == "ultimate":
    from .vendor.ultimate.orchestrator import *  # type: ignore
elif _V == "pro":
    from .vendor.pro.orchestrator import *  # type: ignore
else:
    from .vendor.repo.orchestrator import *  # type: ignore
