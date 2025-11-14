"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

try:
    from .vendor.ultimate.si_utils import *  # type: ignore
except Exception:
    try:
        from .vendor.pro.si_utils import *  # type: ignore
    except Exception:
        from .vendor.repo.si_utils import *  # type: ignore
