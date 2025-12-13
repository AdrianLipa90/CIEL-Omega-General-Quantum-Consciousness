import unittest

from ciel import CielEngine


class TestCielEngineIntegration(unittest.TestCase):
    def test_ciel_engine_step_integration(self) -> None:
        engine = CielEngine()
        engine.boot()
        try:
            result = engine.step("hello world")

            self.assertEqual(result["status"], "ok")
            self.assertIn("simulation", result)
            self.assertIn("tmp_outcome", result)
            self.assertIn("cognition", result)
            self.assertIn("affect", result)
        finally:
            engine.shutdown()


if __name__ == "__main__":
    unittest.main()
