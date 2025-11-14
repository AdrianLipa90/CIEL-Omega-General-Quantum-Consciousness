"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Simplified orchestrator used by the test-suite.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Mapping

from tmp.bifurcation import decide_branch
from tmp.policy import Policy
from tmp.weighting import spectral_weight


@dataclass
class OrchestratedEntry:
    data: str
    weight: float
    status: str
    override: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)


class Orchestrator:
    """A tiny orchestration facade with deterministic behaviour.

    The goal of this class is to provide predictable, easy to reason about
    behaviour for the kata tests without depending on the heavy production
    stack.  The orchestrator keeps a simple in-memory list of temporary
    entries and exposes a ``process_input`` method that mirrors the public
    API of the real component.
    """

    BLOCKED_KEYWORDS = {"wtfblock"}

    def __init__(self) -> None:
        self.tmp_memory: List[OrchestratedEntry] = []
        self.policy = Policy()

    def _features_for(self, data: str) -> Dict[str, Mapping[str, object]]:
        tokens = data.split()
        return {
            "C": {"length": len(data), "tokens": len(tokens)},
            "M": {
                "symbol": tokens[0].lower() if tokens else "",
                "intent": tokens[1].lower() if len(tokens) > 1 else "",
            },
        }

    def process_input(
        self,
        data: str,
        user_subjective: float = 0.0,
        self_subjective: float = 0.0,
        user_save_override: bool = False,
        system_save_override: bool = False,
    ) -> Dict[str, object]:
        raw = (data or "").strip()
        if not raw:
            return {"status": "dropped"}

        lowered = raw.lower()
        if any(keyword in lowered for keyword in self.BLOCKED_KEYWORDS):
            return {"status": "BLOCKED", "reason": "keyword"}

        features = self._features_for(raw)
        tokens = features["C"]["tokens"]
        if tokens < 2 and not (user_save_override or system_save_override):
            return {"status": "WTF", "question": "Not enough context"}

        entry = {"data": raw}
        weight = spectral_weight(entry, features, user_subjective, self_subjective, self.policy)

        if user_save_override or system_save_override:
            result = OrchestratedEntry(data=raw, weight=weight, status="MEM", override=True)
            self.tmp_memory.append(result)
            return {"status": "MEM", "override": True, "weight": weight}

        branch = decide_branch(weight, self.policy.spectral_conf().get("decision"))
        if branch == "mem":
            result = OrchestratedEntry(data=raw, weight=weight, status="MEM")
            self.tmp_memory.append(result)
            return {"status": "MEM", "weight": weight}
        if branch == "out":
            result = OrchestratedEntry(data=raw, weight=weight, status="OUT")
            self.tmp_memory.append(result)
            return {"status": "OUT", "weight": weight}

        result = OrchestratedEntry(data=raw, weight=weight, status="TMP")
        self.tmp_memory.append(result)
        return {"status": "TMP", "weight": weight}


__all__ = ["Orchestrator"]
