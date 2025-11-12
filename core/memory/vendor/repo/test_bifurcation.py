from tmp.bifurcation import decide_branch

def test_bifurcation_thresholds():
    assert decide_branch(1.80)=='mem'
    assert decide_branch(0.70)=='out'
    assert decide_branch(0.10)=='tmp'
