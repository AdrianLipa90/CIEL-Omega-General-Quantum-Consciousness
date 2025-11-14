"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Generate ColourOS inspired descriptors.
"""
from __future__ import annotations

from typing import Dict


def color_tag(m_value: float) -> Dict[str, object]:
    """Return a descriptive colour tag for the given magnitude."""

    if m_value >= 1.5:
        tag = "ultra"
    elif m_value >= 1.0:
        tag = "bright"
    elif m_value >= 0.5:
        tag = "steady"
    else:
        tag = "calm"
    return {"tag": tag, "intensity": float(max(0.0, min(2.0, m_value)))}


__all__ = ["color_tag"]
