"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Basic utilities to load text or binary data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class DataLoader:
    path: Path

    def load_text(self) -> str:
        return Path(self.path).read_text(encoding="utf-8")

    def load_bytes(self) -> bytes:
        return Path(self.path).read_bytes()


__all__ = ["DataLoader"]
