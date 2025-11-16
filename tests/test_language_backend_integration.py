from typing import Any, Dict, List

from ciel import CielEngine
from ciel.language_backend import AuxiliaryBackend, LanguageBackend


class DummyPrimary(LanguageBackend):
    def __init__(self) -> None:
        self.name = "dummy-primary"

    def generate_reply(
        self,
        dialogue: List[Dict[str, str]],
        ciel_state: Dict[str, Any],
    ) -> str:
        return "dummy reply"


class DummyAux(AuxiliaryBackend):
    def __init__(self) -> None:
        self.name = "dummy-aux"

    def analyse_state(
        self,
        ciel_state: Dict[str, Any],
        candidate_reply: str,
    ) -> Dict[str, Any]:
        return {"score": 0.99, "label": "test"}


def test_language_backend_interact_with_dummies():
    engine = CielEngine()
    engine.language_backend = DummyPrimary()
    engine.aux_backend = DummyAux()

    result = engine.interact(
        "hello",
        dialogue=[{"role": "user", "content": "hello"}],
    )

    assert result["status"] == "ok"
    assert result["reply"] == "dummy reply"
    assert "analysis" in result
    assert "ciel_state" in result
