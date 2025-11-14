# Information Flow Pipeline

`integration.information_flow.InformationFlow` links the curated subsystems together:

1. `bio.eeg_processor.EEGProcessor` applies a deterministic low-pass filter to the incoming signal.
2. `bio.crystal_receiver.CrystalFieldReceiver` and `bio.forcing_field.ForcingField` project the
   filtered trace into the intention field.
3. `emotion.eeg_mapper.EEGEmotionMapper` and `emotion.emotion_core.EmotionCore` derive fractional
   band distributions and mood statistics.
4. `fields.soul_invariant.SoulInvariant` evaluates the spectral coherence of the modulated vector.
5. `memory.long_term_memory.LongTermMemory` persists the enriched entry to disk.

The pipeline exposes a single `step(signal)` method that returns the stored entry.  See
`tests/test_information_flow.py` for an executable example.
