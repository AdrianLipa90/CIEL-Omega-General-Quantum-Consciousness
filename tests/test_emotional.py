"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""


import math
import unittest


class TestEmotional(unittest.TestCase):
    def test_emotional_imports(self) -> None:
        from emotion.emotion_core import EmotionCore
        from emotion.eeg_mapper import EEGEmotionMapper

        self.assertIsNotNone(EmotionCore)
        self.assertIsNotNone(EEGEmotionMapper)

    def test_emotion_core_tracks_variance(self) -> None:
        from emotion.emotion_core import EmotionCore

        core = EmotionCore(baseline=0.5)
        result = core.process([0.0, 1.0, 2.0])

        expected_mood = 0.5 + (0.0 + 1.0 + 2.0) / 3.0
        expected_variance = sum((value - result["mood"]) ** 2 for value in [0.0, 1.0, 2.0]) / 3.0

        self.assertAlmostEqual(result["mood"], expected_mood, places=7)
        self.assertAlmostEqual(result["variance"], expected_variance, places=7)

    def test_fractional_distribution_normalises_output(self) -> None:
        from emotion.utils import fractional_distribution

        distribution = fractional_distribution([1.0, 2.0], ["a", "b", "c"])

        self.assertEqual(set(distribution), {"a", "b", "c"})
        self.assertTrue(math.isclose(sum(distribution.values()), 1.0))
        self.assertGreater(distribution["b"], distribution["a"])

    def test_fractional_distribution_handles_negative_values(self) -> None:
        from emotion.utils import fractional_distribution

        distribution = fractional_distribution([-1.0, -3.0], ["alpha", "beta"])

        self.assertAlmostEqual(distribution["beta"], 0.75, places=7)


if __name__ == "__main__":
    unittest.main()
