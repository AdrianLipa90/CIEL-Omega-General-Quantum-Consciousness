"""Utility helpers shared by the compatibility layer."""
from __future__ import annotations

from .color_os import color_tag
from .tensors import encode_tensor_scalar

__all__ = ["color_tag", "encode_tensor_scalar"]
