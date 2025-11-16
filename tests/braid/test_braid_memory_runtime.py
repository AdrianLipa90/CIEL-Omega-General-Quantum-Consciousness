import math

from core.braid import LoopType, make_default_runtime


def test_braid_runtime_coherence_and_scars():
    runtime = make_default_runtime()

    runtime.submit_intention(magnitude=1.0, phase_offset=0.0, loop_type=LoopType.LB)
    runtime.submit_intention(magnitude=1.0, phase_offset=math.pi / 2, loop_type=LoopType.LB)

    results = runtime.step(max_loops=4)

    assert len(results) >= 1
    for loop, success in results:
        assert isinstance(loop.closed, bool)
        assert isinstance(success, bool)

    coherence_value = runtime.memory.coherence()
    assert isinstance(coherence_value, float)

    scar_count = len(runtime.scars.scars)
    assert scar_count >= 1
