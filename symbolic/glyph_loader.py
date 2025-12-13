"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Load glyph data from JSON-like payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import json


@dataclass(slots=True)
class CVOSDatasetLoader:
    path: Path

    def load(self) -> List[dict[str, object]]:
        p = Path(self.path)
        if p.is_dir():
            return []
        if p.suffix.lower() in {".txt"}:
            return self.load_txt(p.name)
        return self.load_json(p.name)

    def _base_dir(self) -> Path:
        p = Path(self.path)
        return p if p.is_dir() else p.parent

    def load_json(self, filename: str) -> List[Dict[str, Any]]:
        p = self._base_dir() / filename
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        if isinstance(data, dict):
            if "sigils" in data:
                value = data["sigils"]
            else:
                value = data.get("glyphs", [])
            return list(value) if isinstance(value, list) else [value]
        if isinstance(data, list):
            return list(data)
        return [data]

    def load_txt(self, filename: str) -> List[Dict[str, Any]]:
        p = self._base_dir() / filename
        entries: List[Dict[str, Any]] = []
        current: Dict[str, Any] = {}
        for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line:
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if k in current:
                entries.append(current)
                current = {}
            current[k] = v
        if current:
            entries.append(current)
        return entries


__all__ = ["CVOSDatasetLoader"]
