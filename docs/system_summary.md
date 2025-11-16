# CIEL-Omega System Summary

## Core Runtime and Orchestration

- `orchestrator.Orchestrator` provides the lightweight policy runtime used by
  tests. It exposes `process_input(...)` and keeps a ledger of
  `OrchestratedEntry` records for TMP/MEM/OUT state transitions.
- `integration.runtime_orchestrator.RuntimeOrchestrator` wraps collectors and
  glue sinks via `BackendAdapter`/`BackendGlue`, running a single
  collector→adapter→sink cycle through `run_once()`.
- `integration.braid_runtime_orchestrator.BraidEnabledRuntime` composes the
  base runtime, `InformationFlow`, and the braid subsystem to optionally extend
  the orchestration pipeline with `BraidRuntime` diagnostics.

## Braid Subsystem (`core/braid/`)

- `memory.py` defines `MemoryUnit` nodes and `BraidMemory` coherence metrics.
- `scars.py` tracks contradiction scars via `Scar` and `ScarRegistry` with
  curvature budgeting.
- `glyphs.py` declares glyph/ritual primitives (`Glyph`, `Ritual`) and their
  engines (`GlyphEngine`, `RitualEngine`).
- `loops.py` models braid loops (`LoopType`, `Loop`) executed by the runtime.
- `phase_field.py` maintains the global phase oscillator for intentions.
- `scheduler.py` orders pending loops under curvature constraints.
- `runtime.py` implements `BraidRuntime`, handling loop construction,
  execution, coherence metrics, and scar registration.
- `adapter.py` exposes `KernelAdapter` for prompt-driven loop submission.
- `defaults.py` provides default glyphs/rituals and `make_default_runtime()`.

## Information Flow Pipeline

- `integration.information_flow.InformationFlow` threads sensor signals through
  the deterministic EEG → intention → emotion → soul-invariant → memory
  pipeline. It uses receivers (`bio.crystal_receiver`), forcing fields,
  emotional cores, and `memory.long_term_memory.LongTermMemory` for
  persistence.

## Memory Orchestration

- `ciel_memory.orchestrator.UnifiedMemoryOrchestrator` manages capture, TMP
  analysis, and long-term persistence, delegating to vendor profiles via
  `core/memory/orchestrator`.
- Vendor selection occurs through `core/memory/vendor` packages, allowing repo,
  pro, or ultimate implementations based on environment configuration.

## Testing Coverage

- Repository tests under `tests/` cover the information flow pipeline,
  Fourier-wave kernel, memory orchestration, and core orchestrators, ensuring
  deterministic behavior across the modular runtime.

