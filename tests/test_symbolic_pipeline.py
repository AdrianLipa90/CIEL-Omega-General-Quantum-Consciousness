from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from symbolic.glyph_interpreter import GlyphNode, GlyphNodeInterpreter
from symbolic.glyph_loader import CVOSDatasetLoader
from symbolic.glyph_pipeline import GlyphPipeline
from symbolic.symbolic_bridge import SymbolicBridge


def test_cvos_dataset_loader_load_json_sigils(tmp_path: Path) -> None:
    payload = {"sigils": [{"name": "alpha", "strokes": 3}]}
    path = tmp_path / "sigils.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    loader = CVOSDatasetLoader(path=path)
    data = loader.load()

    assert isinstance(data, list)
    assert data[0]["name"] == "alpha"


def test_cvos_dataset_loader_load_txt_records(tmp_path: Path) -> None:
    content = "id: 1\nname: foo\nid: 2\nname: bar\n"
    path = tmp_path / "cvos.txt"
    path.write_text(content, encoding="utf-8")

    loader = CVOSDatasetLoader(path=path)
    data = loader.load()

    assert data == [{"id": "1", "name": "foo"}, {"id": "2", "name": "bar"}]


def test_glyph_node_interpreter_registry_executes() -> None:
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

    assert len(outputs) == 1
    assert "Glyph of the First Symphony" in outputs[0]
    assert n1.active is True


def test_glyph_pipeline_combine_and_bridge_color() -> None:
    n1 = GlyphNode(
        id="A",
        name="A",
        code="x",
        field_key="k1",
        operator_signature="op",
    )
    n2 = GlyphNode(
        id="B",
        name="B",
        code="y",
        field_key="k2",
        operator_signature="op",
    )

    loader = CVOSDatasetLoader(path=Path("dummy.json"))
    pipeline = GlyphPipeline(loader=loader)

    sigma = np.ones((4, 4), dtype=float)
    result = pipeline.combine(nodes=[n1, n2], color_weights=[0.6, 0.4], sigma_field=sigma)

    assert set(result.keys()) == {"coherence", "color_mix", "summary"}
    assert result["summary"]
    assert 0.0 <= result["color_mix"] <= 1.0

    bridge = SymbolicBridge(pipeline=pipeline)
    color = bridge.glyph_color(coherence=float(result["coherence"]), sigma_scalar=float(result["coherence"]))

    assert isinstance(color, tuple)
    assert len(color) == 3
    assert all(0.0 <= c <= 1.0 for c in color)
