"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Helpers for encoding tensors in a deterministic format.
"""
from __future__ import annotations

from typing import Iterable, List


def encode_tensor_scalar(weight: float, g_score: float, m_score: float, tokens: int) -> List[float]:
    """Pack the scores into a simple vector."""

    return [float(weight), float(g_score), float(m_score), float(tokens)]


def encode_tensor(values: Iterable[float]) -> List[float]:
    """Return a list copy of ``values`` for compatibility with the vendor API."""

    return [float(v) for v in values]


__all__ = ["encode_tensor", "encode_tensor_scalar"]
