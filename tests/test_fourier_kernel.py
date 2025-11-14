"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import numpy as np

from wave.fourier_kernel import (
    FourierWaveConsciousnessKernel12D,
    KernelSnapshot,
    SimConfig,
)


def test_kernel_generates_snapshot_with_normalised_distribution():
    config = SimConfig(sample_rate=32.0, duration=0.5)
    kernel = FourierWaveConsciousnessKernel12D(config)
    signal = np.linspace(0.0, 1.0, config.sample_count)

    snapshot = kernel.simulate(signal)

    assert isinstance(snapshot, KernelSnapshot)
    assert snapshot.field.shape[0] == config.channels
    assert np.isclose(sum(snapshot.band_distribution.values()), 1.0)
    assert snapshot.purity > 0.0
    assert -1.0 <= snapshot.coherence <= 1.0


def test_kernel_report_returns_latest_summary():
    config = SimConfig(sample_rate=16.0, duration=0.25)
    kernel = FourierWaveConsciousnessKernel12D(config)
    kernel.simulate(np.full(config.sample_count, 10.0))

    report = kernel.report()

    assert "dominant_band" in report
    assert "history_depth" in report
    assert report["history_depth"] == 1
    assert report["samples"] == kernel.history[-1].time_axis.size
