#!/usr/bin/env python3
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from ciel_memory.orchestrator import UnifiedMemoryOrchestrator
if __name__ == "__main__":
    orch = UnifiedMemoryOrchestrator()
    stats = orch.daily_maintenance()
    print("[daily-review]", stats)
