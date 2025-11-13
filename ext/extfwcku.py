"""Test-friendly stub for the spectral wave field module."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SimConfig:
    channels: int = 12
    sample_rate: float = 128.0
    duration: float = 1.0


class FourierWaveConsciousnessKernel12D:
    """Lightweight simulator used to verify imports during testing."""

    def __init__(self, config: SimConfig | None = None) -> None:
        self.config = config or SimConfig()
        self.time_axis: List[float] = []
        self.purity_hist: List[float] = []
        self.entropy_hist: List[float] = []
        self.coh_hist: List[float] = []

    def run(self) -> dict:
        steps = int(self.config.sample_rate * self.config.duration)
        self.time_axis = [i / self.config.sample_rate for i in range(steps)]
        self.purity_hist = [1.0 for _ in self.time_axis]
        self.entropy_hist = [0.0 for _ in self.time_axis]
        self.coh_hist = [1.0 for _ in self.time_axis]
        return {
            "time": self.time_axis,
            "purity": self.purity_hist,
            "entropy": self.entropy_hist,
            "coherence": self.coh_hist,
        }

    def visualize(self, save_path: str | None = None) -> None:  # pragma: no cover - utility method
        self.run()
        if save_path:
            Path(save_path).write_text("visualization placeholder", encoding="utf-8")


class SpectralWaveField12D(FourierWaveConsciousnessKernel12D):
    """Alias kept for backwards compatibility with the vendor API."""


__all__ = ["SpectralWaveField12D", "FourierWaveConsciousnessKernel12D", "SimConfig"]
