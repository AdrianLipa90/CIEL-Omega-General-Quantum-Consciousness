"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from .profile import STORE_VENDOR as _V
if _V == "pro":
    from .vendor.pro.durable_wpm_hdf5 import *  # type: ignore
else:
    from .vendor.ultimate.durable_wpm_hdf5 import *  # type: ignore
