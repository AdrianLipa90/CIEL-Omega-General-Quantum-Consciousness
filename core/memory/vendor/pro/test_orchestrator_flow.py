"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from ciel_memory.orchestrator import UnifiedMemoryOrchestrator
def test_flow_smoke():
    orch = UnifiedMemoryOrchestrator()
    D = orch.capture(context="T", sense="Long enough content to pass analyses.", meta={"novelty_hint": True})
    out = orch.run_tmp(D)
    refs = orch.promote_if_bifurcated(D, out) or orch.user_force_save(D, out, reason="test")
    assert refs and "tsm_ref" in refs and "wpm_ref" in refs
