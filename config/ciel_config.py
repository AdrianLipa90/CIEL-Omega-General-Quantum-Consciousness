"""Runtime configuration objects for the CIEL stack.

The original vendor drop exposed the :class:`CielConfig` dataclass from a
monolithic ``ext`` module.  The tests – and the rest of the package – only need
an ergonomic place where the configuration can be instantiated without pulling
in the raw extensions.  We therefore provide a small, well documented dataclass
here and re-export it from the legacy locations.
"""

from __future__ import annotations

from dataclasses import dataclass
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
