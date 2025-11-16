from __future__ import annotations

from typing import Any, Dict, List, Protocol


class LanguageBackend(Protocol):
    name: str

    def generate_reply(
        self,
        dialogue: List[Dict[str, str]],
        ciel_state: Dict[str, Any],
    ) -> str:
        ...


class AuxiliaryBackend(Protocol):
    name: str

    def analyse_state(
        self,
        ciel_state: Dict[str, Any],
        candidate_reply: str,
    ) -> Dict[str, Any]:
        ...


__all__ = ["LanguageBackend", "AuxiliaryBackend"]
