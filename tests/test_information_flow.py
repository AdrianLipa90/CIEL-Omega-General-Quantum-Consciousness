"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import json
import math
from pathlib import Path

import numpy as np

from integration.information_flow import InformationFlow


def test_information_flow_persists_pipeline(tmp_path):
    storage = tmp_path / "memory.json"
    flow = InformationFlow.build(storage_path=storage, intention_seed=42)

    signal = np.linspace(0.0, 1.0, 16)
    result = flow.step(signal)

    assert set(result) == {
        "filtered",
        "intention",
        "modulated",
        "distribution",
        "emotion",
        "soul_invariant",
    }
    assert math.isclose(sum(result["distribution"].values()), 1.0)
    assert Path(storage).exists()

    saved = json.loads(storage.read_text(encoding="utf-8"))
    assert saved[-1]["emotion"] == result["emotion"]
    assert saved[-1]["distribution"] == result["distribution"]
