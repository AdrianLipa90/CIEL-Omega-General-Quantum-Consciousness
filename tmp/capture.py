"""Capture adapters mirroring the vendor API in a deterministic manner."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(slots=True)
class CaptureEnvelope:
    """Lightweight representation of a captured entry."""

    raw: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    meta: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def as_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "raw": self.raw, "created_at": self.created_at.isoformat(), "meta": self.meta}


def capture(raw: str) -> CaptureEnvelope:
    """Wrap the given raw string inside a :class:`CaptureEnvelope`."""

    return CaptureEnvelope(raw=raw)


__all__ = ["capture", "CaptureEnvelope"]
