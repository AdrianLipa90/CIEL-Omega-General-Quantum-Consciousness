"""Feature extraction routines used by the simplified TMP pipeline."""
from __future__ import annotations

from typing import Dict, Mapping


def analyze_input(raw: str) -> Dict[str, Mapping[str, object]]:
    """Return a deterministic feature dictionary for *raw* input."""

    tokens = raw.split()
    symbol = tokens[0].lower() if tokens else ""
    intent = tokens[1].lower() if len(tokens) > 1 else "general"
    context = "text" if any(ch.isalpha() for ch in raw) else "signal"
    return {
        "C": {"length": len(raw), "tokens": len(tokens)},
        "M": {"symbol": symbol or "default", "intent": intent},
        "T": {"type": context},
    }


__all__ = ["analyze_input"]
