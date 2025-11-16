import pytest

from ciel import CielEngine


def test_ciel_engine_step_integration():
    engine = CielEngine()
    engine.boot()
    try:
        result = engine.step("hello world")

        assert result["status"] == "ok"
        assert "simulation" in result
        assert "tmp_outcome" in result
        assert "cognition" in result
        assert "affect" in result
    finally:
        engine.shutdown()
