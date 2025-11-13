"""Load glyph data from JSON-like payloads."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import json


@dataclass(slots=True)
class CVOSDatasetLoader:
    path: Path

    def load(self) -> List[dict[str, object]]:
        data = json.loads(Path(self.path).read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("glyphs", [])
        return list(data)


__all__ = ["CVOSDatasetLoader"]
