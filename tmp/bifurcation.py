"""Deterministic bifurcation helpers for the kata tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

DEFAULT_TO_MEM = 1.65
DEFAULT_TO_OUT = 0.50


@dataclass(frozen=True)
class DecisionThresholds:
    """Container holding the thresholds used by :func:`decide_branch`."""

    to_mem: float = DEFAULT_TO_MEM
    to_out: float = DEFAULT_TO_OUT

    @classmethod
    def from_mapping(cls, mapping: Optional[dict]) -> "DecisionThresholds":
        if not mapping:
            return cls()
        return cls(
            to_mem=float(mapping.get("to_mem", DEFAULT_TO_MEM)),
            to_out=float(mapping.get("to_out", DEFAULT_TO_OUT)),
        )


def decide_branch(weight: float, thresholds: Optional[DecisionThresholds | dict] = None) -> str:
    """Classify ``weight`` into ``mem``, ``out`` or ``tmp``."""

    if isinstance(thresholds, dict):
        thresholds = DecisionThresholds.from_mapping(thresholds)
    elif thresholds is None:
        thresholds = DecisionThresholds()

    if weight >= thresholds.to_mem:
        return "mem"
    if weight >= thresholds.to_out:
        return "out"
    return "tmp"


__all__ = ["DecisionThresholds", "decide_branch"]
