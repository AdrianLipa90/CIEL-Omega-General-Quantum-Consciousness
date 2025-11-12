import re
from datetime import datetime
from typing import Optional, Tuple
ISO8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$")
def is_iso8601(ts: str) -> bool:
    if not isinstance(ts, str): return False
    if not ISO8601_RE.match(ts):
        try: datetime.fromisoformat(ts); return True
        except Exception: return False
    return True
def validate_timestamp(ts: Optional[str]) -> Tuple[bool, Optional[str]]:
    if not ts: return (False, None)
    if is_iso8601(ts):
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00")) if "Z" in ts else datetime.fromisoformat(ts)
            return (True, dt.isoformat())
        except Exception: return (True, ts)
    return (False, None)
