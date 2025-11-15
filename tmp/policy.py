"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Simplified TMP policy implementation.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


@dataclass(frozen=True)
class _Rule:
    type: str
    value: Iterable[str] | str | None = None
    weight: float = 0.0
    gte: int | None = None
    add: float = 0.0
    symbols: Iterable[str] | None = None
    intents: Iterable[str] | None = None


DEFAULT_CONFIG: Mapping[str, object] = {
    "immutable_rules": [],
    "float_rules_user": [],
    "float_rules_self": [],
    "spectral": {
        "base": 0.4,
        "G_weight": 0.6,
        "M_weight": 0.4,
        "cap_low": 0.0,
        "cap_high": 2.0,
        "decision": {"to_mem": 1.65, "to_out": 0.50},
    },
}


class Policy:
    """Policy facade with a tiny subset of the production behaviour."""

    def __init__(self, path: str | Path | None = "config/policies.json") -> None:
        self.path = Path(path) if path is not None else None
        self.conf: Mapping[str, object] = DEFAULT_CONFIG
        if self.path is not None and self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                loaded = None
            if isinstance(loaded, dict):
                merged = dict(DEFAULT_CONFIG)
                merged.update(loaded)
                self.conf = merged

    # --- immutable boosts -------------------------------------------------
    def immutable_boost(self, data: str, features: Mapping[str, object]) -> float:
        total = 0.0
        for rule in self.conf.get("immutable_rules", []):
            if not isinstance(rule, Mapping):
                continue
            rtype = rule.get("type")
            weight = float(rule.get("weight", 0.0))
            if rtype == "keyword":
                value = str(rule.get("value", "")).lower()
                if value and value in data.lower():
                    total = max(total, weight)
            elif rtype == "tag":
                tags = features.get("M", {}).get("tags", []) if isinstance(features, Mapping) else []
                tag_value = str(rule.get("value", ""))
                if tag_value and tag_value in tags:
                    total = max(total, weight)
        return total

    def float_boost_user(self, data: str, features: Mapping[str, object]) -> float:
        total = 0.0
        for rule in self.conf.get("float_rules_user", []):
            if not isinstance(rule, Mapping):
                continue
            rtype = rule.get("type")
            if rtype == "length_threshold":
                if len(data) >= int(rule.get("gte", 0)):
                    total += float(rule.get("add", 0.0))
            elif rtype == "contains":
                values = rule.get("value", [])
                if any(str(v).lower() in data.lower() for v in values):
                    total += float(rule.get("add", 0.0))
        return total

    def float_boost_self(self, data: str, features: Mapping[str, object]) -> float:
        total = 0.0
        symbol = features.get("M", {}).get("symbol") if isinstance(features, Mapping) else None
        intent = features.get("M", {}).get("intent") if isinstance(features, Mapping) else None
        for rule in self.conf.get("float_rules_self", []):
            if not isinstance(rule, Mapping):
                continue
            rtype = rule.get("type")
            if rtype == "interest_symbol" and symbol in rule.get("symbols", []):
                total += float(rule.get("add", 0.0))
            elif rtype == "intent_match" and intent in rule.get("intents", []):
                total += float(rule.get("add", 0.0))
        return total

    # --- configuration ----------------------------------------------------
    def spectral_conf(self) -> Mapping[str, object]:
        spectral = self.conf.get("spectral", {})
        if not isinstance(spectral, Mapping):
            return DEFAULT_CONFIG["spectral"]
        merged = dict(DEFAULT_CONFIG["spectral"])
        merged.update(spectral)
        decision = dict(DEFAULT_CONFIG["spectral"]["decision"])
        decision.update(spectral.get("decision", {}))
        merged["decision"] = decision
        return merged

    def bias(self) -> Mapping[str, float]:
        return {
            "user": float(self.conf.get("user_bias", 0.0)),
            "system": float(self.conf.get("system_bias", 0.0)),
        }


__all__ = ["Policy", "DEFAULT_CONFIG"]
