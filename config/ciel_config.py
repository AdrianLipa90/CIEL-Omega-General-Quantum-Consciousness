"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Runtime configuration objects for the CIEL stack.

The original vendor drop exposed the :class:`CielConfig` dataclass from a
monolithic ``ext`` module.  The tests – and the rest of the package – only need
an ergonomic place where the configuration can be instantiated without pulling
in the raw extensions.  We therefore provide a small, well documented dataclass
here and re-export it from the legacy locations.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class CielConfig:
    """Light-weight configuration container used across the project.

    The fields mirror the subset that was consumed in the original extension
    modules.  Providing the dataclass in the repository keeps the public API
    stable while making the configuration serialisable and easy to unit test.
    """

    enable_gpu: bool = True
    enable_numba: bool = True
    log_path: Path = Path("logs/reality.jsonl")
    ethics_min_coherence: float = 0.4
    ethics_block_on_violation: bool = True
    dataset_path: Optional[Path] = None

    def load_from_file(self, path: str | Path) -> None:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        raw = p.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("config file must contain a JSON object")
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            if key in {"log_path", "dataset_path"} and value is not None:
                setattr(self, key, Path(value))
            else:
                setattr(self, key, value)

    def as_dict(self) -> dict[str, object]:
        """Return a plain serialisable dictionary representation."""

        return {
            "enable_gpu": self.enable_gpu,
            "enable_numba": self.enable_numba,
            "log_path": str(self.log_path),
            "ethics_min_coherence": self.ethics_min_coherence,
            "ethics_block_on_violation": self.ethics_block_on_violation,
            "dataset_path": str(self.dataset_path) if self.dataset_path else None,
        }


__all__ = ["CielConfig"]
