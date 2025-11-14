"""CIEL/0 — 12D Fourier Wave Consciousness Kernel.

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

This module stitches together the curated field primitives, emotional
statistics and resonance utilities into a lightweight simulation kernel.
It mirrors the narrative of the archival drafts while keeping the
behaviour deterministic and inexpensive enough for the unit test suite.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Sequence

import numpy as np

from emotion.utils import fractional_distribution
from fields.intention_field import IntentionField
from fields.soul_invariant import SoulInvariant
from mathematics.safe_operations import HeisenbergSoftClipper
from resonance.multiresonance_tensor import MultiresonanceTensor

_BAND_LABELS: tuple[str, ...] = (
    "delta",
    "theta",
    "alpha",
    "beta",
    "gamma",
    "lambda",
    "phi",
    "psi",
    "omega",
    "sigma",
    "tau",
    "zeta",
)


@dataclass(slots=True)
class SimConfig:
    """Configuration for the Fourier consciousness kernel."""

    channels: int = 12
    sample_rate: float = 128.0
    duration: float = 1.0
    clip_sigma: float = 4.0
    history: int = 32

    @property
    def sample_count(self) -> int:
        return max(int(round(self.sample_rate * self.duration)), 1)

    @property
    def band_labels(self) -> tuple[str, ...]:
        if self.channels <= len(_BAND_LABELS):
            return _BAND_LABELS[: self.channels]
        return tuple(f"band_{index}" for index in range(self.channels))


@dataclass(slots=True)
class KernelSnapshot:
    """Container describing a single evolution step of the kernel."""

    time_axis: np.ndarray
    field: np.ndarray
    band_distribution: Dict[str, float]
    intention_vector: np.ndarray
    resonance_matrix: np.ndarray
    soul_measure: float
    purity: float
    entropy: float
    coherence: float

    def summary(self) -> Dict[str, float | str]:
        dominant = max(self.band_distribution, key=self.band_distribution.get)
        return {
            "dominant_band": dominant,
            "coherence": float(self.coherence),
            "purity": float(self.purity),
            "entropy": float(self.entropy),
            "soul_measure": float(self.soul_measure),
        }


@dataclass(slots=True)
class SpectralWaveField12D:
    """Generate channel-aligned wave fields with Heisenberg saturation."""

    config: SimConfig = field(default_factory=SimConfig)
    clipper: HeisenbergSoftClipper = field(
        default_factory=HeisenbergSoftClipper, repr=False
    )

    def synthesise(self, signal: Sequence[float] | None) -> tuple[np.ndarray, np.ndarray]:
        samples = self._prepare_signal(signal)
        segments = np.array_split(samples, self.config.channels)
        segment_length = max(segment.size for segment in segments) or 1
        field = np.stack(
            [np.pad(segment, (0, segment_length - segment.size)) for segment in segments]
        )
        time_axis = np.linspace(0.0, self.config.duration, segment_length, endpoint=False)
        return field, time_axis

    def _prepare_signal(self, signal: Sequence[float] | None) -> np.ndarray:
        arr = np.asarray(list(signal) if signal is not None else [], dtype=float)
        target = self.config.sample_count
        if arr.size == 0:
            arr = np.zeros(target, dtype=float)
        elif arr.size < target:
            arr = np.pad(arr, (0, target - arr.size))
        else:
            arr = arr[:target]

        sigma = float(np.std(arr))
        if sigma == 0.0:
            sigma = float(np.max(np.abs(arr)) or 1.0)
        scale = max(self.config.clip_sigma * sigma, 1e-6)
        return self.clipper(arr, scale=scale)


@dataclass(slots=True)
class FourierWaveConsciousnessKernel12D:
    """Integrate the curated subsystems into the 12D kernel."""

    config: SimConfig = field(default_factory=SimConfig)
    intention: IntentionField = field(default_factory=IntentionField)
    soul: SoulInvariant = field(default_factory=SoulInvariant)
    tensor: MultiresonanceTensor = field(default_factory=MultiresonanceTensor)
    spectral: SpectralWaveField12D = field(init=False)
    history: list[KernelSnapshot] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self.spectral = SpectralWaveField12D(self.config)

    def simulate(self, signal: Sequence[float] | None) -> KernelSnapshot:
        field, time_axis = self.spectral.synthesise(signal)
        spectrum = np.abs(np.fft.rfft(field, axis=1))
        band_energy = spectrum.mean(axis=1)
        distribution = fractional_distribution(
            band_energy,
            self.config.band_labels,
            softness=self.config.clip_sigma,
        )

        self.tensor.accumulate(distribution.values())
        resonance_matrix = self.tensor.normalised()

        intention_vector = self.intention.generate()
        projection = self.intention.project(distribution.values())
        coherence = float(np.clip(projection, -1.0, 1.0))

        soul_measure = self.soul.compute(field)
        normalised_field = self.soul.normalise(field)
        purity = float(np.mean(np.square(normalised_field)))

        probs = np.array(list(distribution.values()), dtype=float)
        entropy = float(-np.sum(probs * np.log(probs + 1e-12)))

        snapshot = KernelSnapshot(
            time_axis=time_axis,
            field=normalised_field,
            band_distribution=distribution,
            intention_vector=intention_vector,
            resonance_matrix=resonance_matrix,
            soul_measure=soul_measure,
            purity=purity,
            entropy=entropy,
            coherence=coherence,
        )
        self._store_snapshot(snapshot)
        return snapshot

    def run(self, signals: Iterable[Sequence[float] | None]) -> list[KernelSnapshot]:
        return [self.simulate(signal) for signal in signals]

    def report(self) -> Dict[str, float | str]:
        if not self.history:
            return {}
        latest = self.history[-1]
        summary = latest.summary()
        summary["samples"] = int(latest.time_axis.size)
        summary["history_depth"] = len(self.history)
        return summary

    def _store_snapshot(self, snapshot: KernelSnapshot) -> None:
        self.history.append(snapshot)
        if len(self.history) > self.config.history:
            self.history = self.history[-self.config.history :]


__all__ = [
    "SimConfig",
    "KernelSnapshot",
    "SpectralWaveField12D",
    "FourierWaveConsciousnessKernel12D",
]
