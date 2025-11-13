"""Simple voice memory UI aggregator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class VoiceMemoryUI:
    history: List[str] = field(default_factory=list)

    def record(self, text: str) -> None:
        self.history.append(text)

    def export(self) -> str:
        return "\n".join(self.history)


__all__ = ["VoiceMemoryUI"]
