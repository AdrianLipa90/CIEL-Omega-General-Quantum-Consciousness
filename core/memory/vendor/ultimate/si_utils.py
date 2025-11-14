"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import re
from datetime import datetime
from typing import Optional, Tuple

ISO8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$")

def is_iso8601(ts: str) -> bool:
    if not isinstance(ts, str): return False
    if ISO8601_RE.match(ts): return True
    try:
        _ = datetime.fromisoformat(ts)
        return True
    except Exception:
        return False

def validate_timestamp(ts: Optional[str]) -> Tuple[bool, Optional[str]]:
    if not ts: return (False, None)
    if is_iso8601(ts):
        try:
            if ts.endswith("Z"): return (True, datetime.fromisoformat(ts.replace("Z","+00:00")).isoformat())
            return (True, datetime.fromisoformat(ts).isoformat())
        except Exception: return (True, ts)
    return (False, None)
