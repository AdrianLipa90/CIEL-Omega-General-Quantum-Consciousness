"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Helpers mirroring the vendor spectral weighting API.
"""
from __future__ import annotations

from typing import Dict, Mapping, Tuple

from .policy import Policy
from .weighting import spectral_weight


def compute_weight(
    entry: Mapping[str, object],
    features: Mapping[str, Mapping[str, object]],
    user_subjective: float,
    self_subjective: float,
    policy: Policy,
) -> Tuple[float, float, float, Dict[str, object]]:
    """Compute aggregate scores for ``entry``.

    The real system produces a collection of scores that influence policy
    decisions.  The kata version keeps the behaviour predictable: the spectral
    weight drives the decision and G/M channels simply track the subjective
    contributions.
    """

    weight = spectral_weight(entry, features, user_subjective, self_subjective, policy)
    g_score = max(0.0, min(1.0, user_subjective + policy.bias().get("user", 0.0)))
    m_score = max(0.0, min(1.0, self_subjective + policy.bias().get("system", 0.0)))
    ctx = {
        "symbol": features.get("M", {}).get("symbol", "default"),
        "intent": features.get("M", {}).get("intent", "general"),
    }
    return weight, g_score, m_score, ctx


__all__ = ["compute_weight"]
