# CIEL — Consciousness-Integrated Emergent Logic (Unified Repo)

This repository organizes the uploaded CIEL project drafts into a coherent Python package layout.
Production modules now live in first-party packages; the historic drops remain preserved under
`ext/` for reference but are no longer imported or distributed.

- No placeholders were added to the active code.
- All runtime packages expose deterministic, well tested behaviour.
- Hyphens were normalized to underscores in module filenames.
- Tests verify imports, pipelines and persistence.

> Source provenance: the `ext/` directory contains the raw batch extensions (Ext1 … Ext21, FWCKU,
> Emot, kernels, paradox notes).  They stay untouched as archival material.  The Python package
> published by `setup.py` excludes those modules and instead uses the curated equivalents under
> `bio/`, `emotion/`, `fields/`, `memory/`, `integration/`, etc.

## Information Flow Pipeline

`integration.information_flow.InformationFlow` wires the biological receivers, emotional analysis,
field primitives and memory persistence into a deterministic pipeline.  Each call to
`InformationFlow.step` filters an incoming sensor signal, projects it into the intention field,
computes emotional statistics, evaluates the soul invariant metric and persists the enriched entry
to long term memory.

The orchestrated pipeline keeps the original intent of the drafts (EEG ➜ intention ➜ emotion ➜
memory) while avoiding the heavyweight vendor dependencies.  See `tests/test_information_flow.py`
for usage examples.


## Heisenberg Soft Clip Operator

Numerical safeguards that previously relied on hard `numpy.clip` calls now delegate to the
`mathematics.safe_operations.heisenberg_soft_clip*` helpers.  The Heisenberg-inspired saturation
keeps small amplitudes perfectly linear while smoothly approaching the configured limits for large
values.  The behaviour mirrors the repository narrative: pushing an observable harder increases the
uncertainty instead of snapping to an abrupt bound.  See `tests/test_soft_clip.py` for the sanity
checks that cover both the symmetric and ranged variants.


## Fourier Wave Consciousness Kernel

`wave.fourier_kernel.FourierWaveConsciousnessKernel12D` combines the curated intention, emotion,
resonance and soul primitives into a deterministic twelve-channel simulation.  The helper exposes a
`simulate` method that soft-saturates incoming signals using the Heisenberg operator, projects them
into EEG-like bands, updates the resonance tensor and summarises the soul invariant.  The
`report()` API returns a compact summary with the dominant band, coherence level and history depth so
tests can verify the end-to-end flow.  See `tests/test_fourier_kernel.py` for an executable example.


## Memory Vendor Selector
All user memory modules are bundled under `core/memory/vendor/{ultimate,pro,repo}`.
Wrappers in `core/memory/*.py` import from a selected vendor via env var:
```
export CIEL_MEM_VENDOR=ultimate   # or pro, repo
```
Defaults: orchestrator->repo, stores->ultimate, policy->ultimate.

## License & Diagnostics

All active Python modules now declare the canonical CIEL Research Non-Commercial License v1.1 header
and updated copyright attribution for Adrian Lipa / Intention Lab.  The migration was accompanied by a
full repository test sweep (`pytest`) to validate the orchestration, memory pipelines and Fourier
kernel—see the Testing section in this README and the project documentation for reproducible
commands.  Consumers should retain these headers in derived work and refer to `LICENSE` for the full
terms.
