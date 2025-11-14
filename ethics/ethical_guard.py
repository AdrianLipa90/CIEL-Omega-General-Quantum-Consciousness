"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Deterministic guard that checks coherence and ethical constraints.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EthicsGuard:
    """Small helper enforcing minimum coherence and ethics flags."""

    bound: float = 0.90
    min_coherence: float = 0.4
    block: bool = True

    def check_step(self, coherence: float, ethical_ok: bool, info_fidelity: float) -> None:
        if coherence < self.min_coherence or not ethical_ok:
            msg = (
                f"[EthicsGuard] breach: coherence={coherence:.3f} "
                f"ethical_ok={ethical_ok} fidelity={info_fidelity:.3f}"
            )
            if self.block:
                raise RuntimeError(msg)
            print("⚠", msg)


__all__ = ["EthicsGuard"]
