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


## Memory Vendor Selector
All user memory modules are bundled under `core/memory/vendor/{ultimate,pro,repo}`.
Wrappers in `core/memory/*.py` import from a selected vendor via env var:
```
export CIEL_MEM_VENDOR=ultimate   # or pro, repo
```
Defaults: orchestrator->repo, stores->ultimate, policy->ultimate.
