from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class MemoriseD:
    memorise_id: str
    created_at: str
    D_id: str
    D_context: str
    D_sense: Any
    D_associations: List[Any]
    D_timestamp: str
    D_meta: Dict[str, Any]
    D_type: str
    D_attr: Dict[str, Any]
    weights: Dict[str, Any]
    rationale: str = ""
    source: str = "TMP"
