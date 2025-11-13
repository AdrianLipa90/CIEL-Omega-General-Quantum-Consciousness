"""Tiny backend adapter orchestrating capture of metrics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any


@dataclass(slots=True)
class BackendAdapter:
    collector: Callable[[], Dict[str, Any]]
    last_payload: Dict[str, Any] = field(default_factory=dict, init=False)

    def run(self) -> Dict[str, Any]:
        self.last_payload = self.collector()
        return self.last_payload


__all__ = ["BackendAdapter"]
