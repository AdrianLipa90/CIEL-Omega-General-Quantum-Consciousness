"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

High level information flow pipeline without vendor extensions.

The raw `ext/` directory contains uncurated drops of the historical
implementation.  The active codebase builds a much smaller, deterministic
subset so tests and exercises can run without importing from those raw files.

`InformationFlow` stitches together the bio, emotion, field and memory
components into a reproducible pipeline.  The class exposes a single ``step``
method that accepts an arbitrary iterable of floats representing a sensor
signal.  The signal is filtered, projected into the intention field, analysed
by the emotional core and finally persisted to long term memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable

import numpy as np

from bio.crystal_receiver import CrystalFieldReceiver
from bio.eeg_processor import EEGProcessor
from bio.forcing_field import ForcingField
from emotion.eeg_mapper import EEGEmotionMapper
from emotion.emotion_core import EmotionCore
from fields.intention_field import IntentionField
from fields.soul_invariant import SoulInvariant
from memory.long_term_memory import LongTermMemory


@dataclass(slots=True)
class InformationFlow:
    """Compose the lightweight subsystems into a single pipeline."""

    receiver: CrystalFieldReceiver
    forcing: ForcingField
    eeg: EEGProcessor
    mapper: EEGEmotionMapper
    emotion: EmotionCore
    memory: LongTermMemory
    soul: SoulInvariant = field(default_factory=SoulInvariant)

    @classmethod
    def build(
        cls,
        *,
        storage_path: Path,
        intention_seed: int | None = None,
        baseline: float = 0.0,
        sample_rate: float = 128.0,
    ) -> "InformationFlow":
        """Create a fully wired pipeline with deterministic defaults."""

        intention = IntentionField(seed=intention_seed)
        return cls(
            receiver=CrystalFieldReceiver(intention),
            forcing=ForcingField(intention),
            eeg=EEGProcessor(sample_rate=sample_rate),
            mapper=EEGEmotionMapper(),
            emotion=EmotionCore(baseline=baseline),
            memory=LongTermMemory(storage_path),
        )

    def step(self, signal: Iterable[float]) -> Dict[str, Any]:
        """Process *signal* through the entire information pipeline."""

        filtered = self.eeg.filter(signal)
        prepared = self._match_channels(filtered)
        intention_vector = self.receiver.receive(prepared)
        modulated = self.forcing.stimulate(prepared)
        emotional_input = modulated if modulated.size else intention_vector

        distribution = self.mapper.map(emotional_input)
        emotion_state = self.emotion.process(emotional_input)
        invariant_value = self.soul.compute(self._reshape_for_invariant(emotional_input))

        entry = {
            "filtered": prepared.tolist(),
            "intention": intention_vector.tolist(),
            "modulated": emotional_input.tolist(),
            "distribution": distribution,
            "emotion": emotion_state,
            "soul_invariant": invariant_value,
        }
        self.memory.store(entry)
        return entry

    @staticmethod
    def _reshape_for_invariant(vector: np.ndarray) -> np.ndarray:
        """Create a 2D matrix compatible with :class:`SoulInvariant`."""

        size = vector.size
        if size == 0:
            return np.zeros((2, 2))
        side = int(np.ceil(np.sqrt(size)))
        padded = np.pad(vector, (0, side * side - size), mode="constant", constant_values=0.0)
        return padded.reshape(side, side)

    def _match_channels(self, signal: np.ndarray) -> np.ndarray:
        """Fit ``signal`` to the intention channel count."""

        channels = self.receiver.intention.channels
        if signal.size >= channels:
            return signal[:channels]
        if signal.size == 0:
            return signal
        return np.pad(signal, (0, channels - signal.size), mode="constant", constant_values=0.0)


__all__ = ["InformationFlow"]
