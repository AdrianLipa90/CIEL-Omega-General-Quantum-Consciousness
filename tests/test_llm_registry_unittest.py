from __future__ import annotations

import unittest


class TestLLMRegistry(unittest.TestCase):
    def test_build_default_bundle_and_select(self) -> None:
        from ciel.llm_registry import build_default_bundle

        bundle = build_default_bundle()

        self.assertTrue(hasattr(bundle.lite, "generate_reply"))
        self.assertTrue(hasattr(bundle.standard, "generate_reply"))
        self.assertTrue(hasattr(bundle.science, "generate_reply"))

        primary = bundle.primary_for("lite")
        self.assertIsNotNone(primary)

    def test_composite_aux_merges(self) -> None:
        from ciel.llm_registry import CompositeAuxBackend
        from ciel.language_backend import AuxiliaryBackend

        class A(AuxiliaryBackend):
            def __init__(self) -> None:
                self.name = "a"

            def analyse_state(self, ciel_state, candidate_reply):
                return {"x": 1}

        class B(AuxiliaryBackend):
            def __init__(self) -> None:
                self.name = "b"

            def analyse_state(self, ciel_state, candidate_reply):
                return {"y": 2}

        aux = CompositeAuxBackend(backends=[A(), B()])
        out = aux.analyse_state({"state": True}, "reply")

        self.assertEqual(out["a"]["x"], 1)
        self.assertEqual(out["b"]["y"], 2)


if __name__ == "__main__":
    unittest.main()
