"""Utility helpers for sanitising raw inputs before TMP processing."""
from __future__ import annotations

from typing import Optional


def prefilter(data: object | None) -> Optional[str]:
    """Return a normalised string or ``None`` when the input is empty.

    The historical implementation performed a large amount of normalisation
    work.  For the purposes of the kata we only need deterministic behaviour:
    ``None``/whitespace inputs yield ``None`` and everything else is stripped of
    leading/trailing whitespace.
    """

    if data is None:
        return None
    if isinstance(data, bytes):
        text = data.decode("utf-8", errors="ignore")
    else:
        text = str(data)
    text = text.strip()
    return text or None


__all__ = ["prefilter"]
