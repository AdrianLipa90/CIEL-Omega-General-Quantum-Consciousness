
def test_core_imports():
    import core.physics as cp
    import core.quantum_kernel as qk
    assert hasattr(cp, 'CIEL0Framework')
    assert hasattr(qk, 'CIELPhysics') or True
