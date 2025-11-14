"""Back-end glue combining capture, analysis and persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any


@dataclass(slots=True)
class BackendGlue:
    callback: Callable[[Dict[str, Any]], None]
    history: list[Dict[str, Any]] = field(default_factory=list, init=False)

    def emit(self, payload: Dict[str, Any]) -> None:
        self.history.append(payload)
        self.callback(payload)


__all__ = ["BackendGlue"]
