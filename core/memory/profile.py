"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import os
VENDOR = os.environ.get("CIEL_MEM_VENDOR", "").strip().lower()
ORCH_VENDOR   = VENDOR or "repo"
POLICY_VENDOR = VENDOR or "ultimate"
STORE_VENDOR  = VENDOR or "ultimate"


def _normalise_vendor(value: str) -> str:
    return (value or "").strip().lower()


def get_memory_vendor() -> str:
    return _normalise_vendor(os.environ.get("CIEL_MEM_VENDOR", ""))


def get_orchestrator_vendor(default: str = "repo") -> str:
    value = get_memory_vendor() or default
    if value not in {"repo", "pro", "ultimate"}:
        return default
    return value


def get_policy_vendor(default: str = "ultimate") -> str:
    value = get_memory_vendor() or default
    if value not in {"repo", "pro", "ultimate"}:
        return default
    return value


def get_store_vendor(default: str = "ultimate") -> str:
    value = get_memory_vendor() or default
    if value not in {"repo", "pro", "ultimate"}:
        return default
    return value


__all__ = [
    "VENDOR",
    "ORCH_VENDOR",
    "POLICY_VENDOR",
    "STORE_VENDOR",
    "get_memory_vendor",
    "get_orchestrator_vendor",
    "get_policy_vendor",
    "get_store_vendor",
]
