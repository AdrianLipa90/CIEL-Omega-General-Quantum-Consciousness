"""Interfaces describing numerical kernels used by the simulations."""

from __future__ import annotations

from typing import Protocol, Sequence


class KernelSpec(Protocol):
    """Protocol describing the public surface of a simulation kernel."""

    grid_size: int
    time_steps: int
    constants: Sequence[float]

    def evolve_reality(self, steps: int | None = None) -> dict[str, list[float]]:
        """Advance the simulation and return diagnostic metrics."""

    def update_reality_fields(self) -> None:
        """Refresh cached field values after an evolution step."""

    def normalize_field(self, field) -> None:
        """Normalise the supplied field in-place."""


__all__ = ["KernelSpec"]
