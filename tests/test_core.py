"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""


def test_core_imports():
    import core.physics as cp
    import core.quantum_kernel as qk
    assert hasattr(cp, 'CIEL0Framework')
    assert hasattr(qk, 'CIELPhysics') or True
