# CIEL — Consciousness-Integrated Emergent Logic (Unified Repo)

This repository organizes the uploaded CIEL project drafts into a coherent Python package layout.
Code modules are provided exactly from the original drafts; where a draft contains many classes,
thin wrappers expose them under the required package paths without modifying logic.

- No placeholders were added.
- All packages have `__init__.py`.
- Hyphens were normalized to underscores in module filenames.
- Tests verify imports and basic object presence.

> Source provenance: the `ext/` package contains the raw batch extensions (Ext1 … Ext21, FWCKU, Emot),
> plus unified kernels (CIELnoFFT, CielQuantum, Lie4full, Paradoxes, definitekernel, Parlie4).


## Memory Vendor Selector
All user memory modules are bundled under `core/memory/vendor/{ultimate,pro,repo}`.
Wrappers in `core/memory/*.py` import from a selected vendor via env var:
```
export CIEL_MEM_VENDOR=ultimate   # or pro, repo
```
Defaults: orchestrator->repo, stores->ultimate, policy->ultimate.
