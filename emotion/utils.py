"""Shared utilities for the lightweight emotion modules.

The repo previously duplicated a couple of signal-processing helpers across the
emotional primitives.  Centralising the helpers keeps the behaviour aligned
between the mapper and the core without depending on the large vendor
extensions.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def to_signal_list(signal: Iterable[float]) -> List[float]:
    """Coerce an arbitrary iterable of numbers into a concrete ``list``.

    The helper is intentionally forgiving – any falsy or ``None`` values are
    ignored so callers can pass data directly from mocked hardware streams.
    """

    values: List[float] = []
    for value in signal:
        if value is None:
            continue
        values.append(float(value))
    return values


def mean_and_variance(values: Sequence[float], *, baseline: float = 0.0) -> Tuple[float, float]:
    """Compute mean and (population) variance for a sequence of floats.

    Parameters
    ----------
    values:
        Sequence of numeric values.  If empty the baseline is returned as the
        mean and the variance defaults to ``0.0``.
    baseline:
        Optional baseline value that is blended with the empirical mean.  This
        keeps the behaviour consistent with the simplified vendor expectation
        where a neutral mood may be configured externally.
    """

    if not values:
        return baseline, 0.0

    mean = baseline + sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return mean, variance


def fractional_distribution(values: Sequence[float], labels: Sequence[str]) -> dict[str, float]:
    """Return a normalised fractional distribution indexed by ``labels``.

    The helper pads or truncates the source ``values`` so it gracefully handles
    signals that do not perfectly match the set of EEG bands used in the tests.
    Negative values are converted to their absolute magnitude so callers can
    provide pre-processed FFT outputs without worrying about sign conventions.
    """

    if not labels:
        return {}

    counts = [abs(float(value)) for value in values if value is not None]
    counts = counts or [1.0]

    expanded = [counts[i % len(counts)] for i in range(len(labels))]
    total = sum(expanded) or 1.0

    return {
        band: expanded[i] / total
        for i, band in enumerate(labels)
    }


__all__ = [
    "to_signal_list",
    "mean_and_variance",
    "fractional_distribution",
]

