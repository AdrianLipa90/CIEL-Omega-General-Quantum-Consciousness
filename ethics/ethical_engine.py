"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Compact ethical engine used by the tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


@dataclass(slots=True)
class EthicalEngine:
    """Score sentences using a rule based sentiment heuristic."""

    positive_words: Iterable[str] = ("love", "peace", "harmony")
    negative_words: Iterable[str] = ("hate", "war", "chaos")
    history: list[Dict[str, float]] = field(default_factory=list, init=False, repr=False)

    def evaluate(self, text: str) -> Dict[str, float]:
        words = text.lower().split()
        pos = sum(words.count(w) for w in self.positive_words)
        neg = sum(words.count(w) for w in self.negative_words)
        score = (pos - neg) / max(len(words), 1)
        coherence = 1.0 - min(abs(score), 1.0) * 0.5
        result = {"score": score, "coherence": coherence}
        self.history.append(result)
        return result


__all__ = ["EthicalEngine"]
