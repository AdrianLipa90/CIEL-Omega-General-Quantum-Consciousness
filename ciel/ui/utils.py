from __future__ import annotations

import json
from typing import Any


def dig(obj: Any, *path: str, default: Any = None) -> Any:
    cur: Any = obj
    for key in path:
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(key)
        else:
            cur = getattr(cur, key, None)
    return default if cur is None else cur


def pretty_json(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


__all__ = ["dig", "pretty_json"]
