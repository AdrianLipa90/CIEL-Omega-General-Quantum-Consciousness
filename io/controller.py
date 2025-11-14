"""Realtime controller orchestrating audio/text updates."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List


@dataclass(slots=True)
class RealTimeController:
    callbacks: List[Callable[[str], None]] = field(default_factory=list)

    def register(self, callback: Callable[[str], None]) -> None:
        self.callbacks.append(callback)

    def dispatch(self, message: str) -> None:
        for cb in self.callbacks:
            cb(message)


__all__ = ["RealTimeController"]
