from datetime import datetime
from typing import Any, Dict

def capture(data: Any, source: str = "user", channel: str = "text") -> Dict:
    """Capture raw input with minimal, immutable metadata."""
    return {
        "data": data,
        "meta": {
            "source": source,
            "channel": channel,
            "timestamp": datetime.utcnow().isoformat(timespec='seconds'),
        }
    }
