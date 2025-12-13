from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class KernelSpec(Protocol):
    """Minimalny interfejs, by uruchamiać A/B porównania rdzeni."""
    grid_size: int
    time_steps: int
    constants: Any

    def evolve_reality(self, steps: Optional[int]=None) -> Dict[str, List[float]]:
        ...

    def update_reality_fields(self) -> None:
        ...

    def normalize_field(self, field: np.ndarray) -> None:
        ...