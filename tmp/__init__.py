"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Lightweight compatibility layer for memory vendor tests.
"""
from __future__ import annotations

from .analysis import analyze_input
from .bifurcation import decide_branch
from .capture import capture
from .heuristics import Heuristics
from .policy import Policy
from .prefilter import prefilter
from .reports import daily_report
from .spectral_weighting import compute_weight
from .weighting import spectral_weight

__all__ = [
    "analyze_input",
    "capture",
    "compute_weight",
    "daily_report",
    "decide_branch",
    "Heuristics",
    "Policy",
    "prefilter",
    "spectral_weight",
]
