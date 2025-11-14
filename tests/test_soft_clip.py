import numpy as np

from mathematics.safe_operations import heisenberg_soft_clip, heisenberg_soft_clip_range


def test_heisenberg_soft_clip_behaves_linearly_for_small_values():
    x = np.linspace(-0.1, 0.1, 5)
    y = heisenberg_soft_clip(x, scale=1.0)
    assert np.allclose(y, x, atol=1e-3)


def test_heisenberg_soft_clip_saturates_extremes():
    y = heisenberg_soft_clip(np.array([-10.0, 10.0]), scale=1.0)
    assert np.all(np.abs(y) < 1.0)
    assert np.all(np.abs(y) > 0.75)


def test_heisenberg_soft_clip_range_respects_bounds():
    values = heisenberg_soft_clip_range(np.array([-5.0, 0.0, 5.0]), 0.0, 2.0)
    assert np.all(values >= 0.0)
    assert np.all(values <= 2.0)
