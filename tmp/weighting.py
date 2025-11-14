"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Spectral weighting helpers used in the tests.
"""
from __future__ import annotations

from typing import Mapping, Tuple

from .policy import Policy


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _compute_components(
    entry: Mapping[str, object],
    features: Mapping[str, Mapping[str, object]],
    user_subjective: float,
    self_subjective: float,
    policy: Policy,
) -> Tuple[float, float, float]:
    data = entry.get("data", "")
    ctx = features.get("C", {}) if isinstance(features, Mapping) else {}
    meta = features.get("M", {}) if isinstance(features, Mapping) else {}
    tokens = float(ctx.get("tokens", 0) or 0)
    length = float(ctx.get("length", 0) or 0)

    # Global (G) score prefers longer content and richer phrasing.
    diversity = len(set(str(data).split()))
    G = min(1.0, (tokens / 6.0) + (diversity / 20.0) + (length / 300.0))

    # Meaning (M) score reacts to metadata and novelty hints.
    novelty = 1.0 if meta.get("intent") else 0.5
    if meta.get("symbol"):
        novelty += 0.2
    if isinstance(meta.get("tags"), (list, tuple, set)) and meta["tags"]:
        novelty += 0.1
    M = clamp(novelty, 0.0, 1.2)

    conf = policy.spectral_conf()
    base = float(conf.get("base", 0.4))
    G_weight = float(conf.get("G_weight", 0.6))
    M_weight = float(conf.get("M_weight", 0.4))
    cap_low = float(conf.get("cap_low", 0.0))
    cap_high = float(conf.get("cap_high", 2.0))

    immutable = policy.immutable_boost(data, features)
    user_boost = policy.float_boost_user(data, features) * max(user_subjective, 0.0)
    self_boost = policy.float_boost_self(data, features) * max(self_subjective, 0.0)

    subjective = max(-0.5, user_subjective) + max(-0.5, self_subjective)

    weight = base + (G_weight * G) + (M_weight * M) + immutable + user_boost + self_boost + subjective
    weight = clamp(weight, cap_low, cap_high)
    return weight, G, M


def spectral_weight(
    entry: Mapping[str, object],
    features: Mapping[str, Mapping[str, object]],
    user_subjective: float = 0.0,
    self_subjective: float = 0.0,
    policy: Policy | None = None,
) -> float:
    """Compute a simplified spectral weight for the tests."""

    policy = policy or Policy()
    weight, _, _ = _compute_components(entry, features, user_subjective, self_subjective, policy)
    return weight


def decision_thresholds(policy: Policy | None = None) -> Mapping[str, float]:
    conf = (policy or Policy()).spectral_conf()
    decision = conf.get("decision", {})
    return {
        "to_mem": float(decision.get("to_mem", 1.65)),
        "to_out": float(decision.get("to_out", 0.50)),
    }


__all__ = ["spectral_weight", "decision_thresholds", "clamp"]
