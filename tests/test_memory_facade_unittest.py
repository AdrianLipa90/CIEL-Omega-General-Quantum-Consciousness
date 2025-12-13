from __future__ import annotations

import unittest


class TestMemoryFacade(unittest.TestCase):
    def test_build_orchestrator_returns_object(self) -> None:
        from core.memory.facade import build_orchestrator

        orch = build_orchestrator()
        self.assertIsNotNone(orch)
        self.assertTrue(hasattr(orch, "capture"))
        self.assertTrue(hasattr(orch, "run_tmp"))


if __name__ == "__main__":
    unittest.main()
