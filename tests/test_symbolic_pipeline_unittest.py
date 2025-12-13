from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from symbolic.glyph_interpreter import GlyphNode, GlyphNodeInterpreter
from symbolic.glyph_loader import CVOSDatasetLoader
from symbolic.glyph_pipeline import GlyphPipeline
from symbolic.symbolic_bridge import SymbolicBridge


class TestSymbolicPipeline(unittest.TestCase):
    def test_cvos_dataset_loader_load_json_sigils(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            payload = {"sigils": [{"name": "alpha", "strokes": 3}]}
            path = tmp_path / "sigils.json"
            path.write_text(json.dumps(payload), encoding="utf-8")

            loader = CVOSDatasetLoader(path=path)
            data = loader.load()

            self.assertIsInstance(data, list)
            self.assertEqual(data[0]["name"], "alpha")

    def test_cvos_dataset_loader_load_txt_records(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            content = "id: 1\nname: foo\nid: 2\nname: bar\n"
            path = tmp_path / "cvos.txt"
            path.write_text(content, encoding="utf-8")

            loader = CVOSDatasetLoader(path=path)
            data = loader.load()

            self.assertEqual(data, [{"id": "1", "name": "foo"}, {"id": "2", "name": "bar"}])

    def test_glyph_node_interpreter_registry_executes(self) -> None:
        n1 = GlyphNode(
            id="GLIF_GEN.01C",
            name="Glyph of the First Symphony",
            code="intent.sound[α₁] >> field.init(resonance)",
            field_key="CVOS::GENESIS_01",
            operator_signature="INT::LIPA.001",
        )

        interp = GlyphNodeInterpreter()
        interp.register(n1)

        outputs = interp.execute_sequence(["GLIF_GEN.01C", "MISSING"])

        self.assertEqual(len(outputs), 1)
        self.assertIn("Glyph of the First Symphony", outputs[0])
        self.assertTrue(n1.active)

    def test_glyph_pipeline_combine_and_bridge_color(self) -> None:
        n1 = GlyphNode(id="A", name="A", code="x", field_key="k1", operator_signature="op")
        n2 = GlyphNode(id="B", name="B", code="y", field_key="k2", operator_signature="op")

        loader = CVOSDatasetLoader(path=Path("dummy.json"))
        pipeline = GlyphPipeline(loader=loader)

        sigma = np.ones((4, 4), dtype=float)
        result = pipeline.combine(nodes=[n1, n2], color_weights=[0.6, 0.4], sigma_field=sigma)

        self.assertEqual(set(result.keys()), {"coherence", "color_mix", "summary"})
        self.assertTrue(result["summary"])
        self.assertGreaterEqual(result["color_mix"], 0.0)
        self.assertLessEqual(result["color_mix"], 1.0)

        bridge = SymbolicBridge(pipeline=pipeline)
        color = bridge.glyph_color(coherence=float(result["coherence"]), sigma_scalar=float(result["coherence"]))

        self.assertIsInstance(color, tuple)
        self.assertEqual(len(color), 3)
        self.assertTrue(all(0.0 <= c <= 1.0 for c in color))


if __name__ == "__main__":
    unittest.main()
