"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Simple heuristics used by the orchestrator facade.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Tuple


@dataclass(slots=True)
class Heuristics:
    """Very small blocker detector.

    The heuristic simply checks whether any forbidden tokens are present in the
    analysed string.  The API mirrors the original implementation used by the
    vendor packages.
    """

    blocked_tokens: Iterable[str] = field(default_factory=lambda: {"wtfblock", "forbidden"})

    def check_blockers(self, raw: str) -> Tuple[bool, str | None]:
        lowered = raw.lower()
        for token in self.blocked_tokens:
            if token in lowered:
                return True, f"contains:{token}"
        return False, None


__all__ = ["Heuristics"]
