"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import os
VENDOR = os.environ.get("CIEL_MEM_VENDOR", "").strip().lower()
ORCH_VENDOR   = VENDOR or "repo"
POLICY_VENDOR = VENDOR or "ultimate"
STORE_VENDOR  = VENDOR or "ultimate"
