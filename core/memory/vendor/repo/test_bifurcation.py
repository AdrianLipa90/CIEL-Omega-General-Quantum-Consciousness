"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from tmp.bifurcation import decide_branch

def test_bifurcation_thresholds():
    assert decide_branch(1.80)=='mem'
    assert decide_branch(0.70)=='out'
    assert decide_branch(0.10)=='tmp'
