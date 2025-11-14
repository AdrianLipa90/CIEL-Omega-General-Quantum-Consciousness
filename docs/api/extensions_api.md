# Extensions API

The `ext/` directory ships the raw reference drops uploaded with the project.  They are intentionally
kept out of the active Python package so experiments can run against the deterministic re-implementations
under `bio/`, `emotion/`, `fields/`, `memory/`, and `integration/`.

For maintained entry points see:

- `fields.intention_field.IntentionField` and `fields.soul_invariant.SoulInvariant` for the core
  field mathematics.
- `emotion.utils` and `emotion.emotion_core` for the lightweight affective analysis helpers.
- `integration.information_flow.InformationFlow` to observe the full EEG ➜ intention ➜ emotion ➜
  memory pipeline without touching the archival modules.