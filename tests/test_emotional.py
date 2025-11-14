
import math

import pytest


def test_emotional_imports():
    from emotion.emotion_core import EmotionCore
    from emotion.eeg_mapper import EEGEmotionMapper

    assert EmotionCore is not None and EEGEmotionMapper is not None


def test_emotion_core_tracks_variance():
    from emotion.emotion_core import EmotionCore

    core = EmotionCore(baseline=0.5)
    result = core.process([0.0, 1.0, 2.0])

    assert result["mood"] == pytest.approx(0.5 + (0.0 + 1.0 + 2.0) / 3.0)
    assert result["variance"] == pytest.approx(
        sum((value - result["mood"]) ** 2 for value in [0.0, 1.0, 2.0]) / 3.0
    )


def test_fractional_distribution_normalises_output():
    from emotion.utils import fractional_distribution

    distribution = fractional_distribution([1.0, 2.0], ["a", "b", "c"])

    assert set(distribution) == {"a", "b", "c"}
    assert math.isclose(sum(distribution.values()), 1.0)
    assert distribution["b"] > distribution["a"]


def test_fractional_distribution_handles_negative_values():
    from emotion.utils import fractional_distribution

    distribution = fractional_distribution([-1.0, -3.0], ["alpha", "beta"])

    assert distribution["beta"] == pytest.approx(0.75)
