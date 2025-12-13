# CIEL/Ω — General Quantum Consciousness System  
### *Extended README — Full Scientific, Mathematical & Architectural Documentation*
A. Lipa, S. Sakpal, M. Kamecka, U. Ahmad (2025). (c) 2025 Adrian Lipa / Intention Lab
---

## README 1.1 — Trust-First Overview (Reality-Backed)

This file is the *strategic* and *adoption-focused* README.

- For a **component-by-component technical map**, see `readme2.md`.
- For **installation and running instructions**, see `hints.md`.

CIEL/Ω is a deterministic, testable framework that integrates:

- wave-field simulation (12D Fourier kernel)
- intention fields and coherence metrics
- cognition and affect modules
- ethical gating (hard-stop constraints)
- memory orchestration (vendor profiles)
- optional language backends (LLM as an expression layer, not a reasoning core)

It is designed for one purpose: **rebuilding trust in AI-assisted reasoning by making the *core* of the system measurable, stable, and ethically non-negotiable**.

---

## Why CIEL/Ω exists

We are living through an era of extreme social polarization and a rapidly expanding “trust crisis” around AI.

In high-stakes environments—government, medicine, pharma, education, critical business decisions—many AI systems are currently disqualified for a simple reason:

- they **drift** over time,
- they develop **semantic sloppiness** under pressure,
- they produce **hallucinations** that look confident,
- and they cannot reliably maintain a stable decision boundary.

Even when these systems are powerful, they are often not acceptable as strategic instruments because they fail the fundamental requirement of mission-critical systems:

- **repeatability**
- **measurable constraints**
- **auditability**

CIEL/Ω was created to be the opposite of “black box autopilot AI”.

It is a framework where the *core intelligence layer* is **not a free-form generator**. The generator (LLM) is optional and remains a controlled interface.

---

## Ethics is a non-negotiable condition of existence

CIEL/Ω treats ethics as a *hard constraint*, not a “prompt”.

- Ethics is not a feature.
- Ethics is **the condition under which the system is allowed to run**.

### What “hard constraint” means in this codebase

The project implements a deterministic guard (`ethics/EthicsGuard`) configured by `config/CielConfig`.

- A minimum coherence threshold is defined (`ethics_min_coherence`).
- If a step falls below the threshold or the ethical evaluation fails, the guard triggers a **hard stop** (default behavior is to raise an exception).

This enforces the intended invariant:

> **Any attempt to push the ethical gradient below the minimum bound deactivates the system’s execution path.**

In the conceptual language of the repository, this is also represented by the Λ₀ protective operator (`ethics/Lambda0Operator`).

---

## What makes CIEL/Ω different from typical AI stacks

### Deterministic core

The curated runtime modules are intentionally deterministic and covered by tests. This means:

- the same input yields the same pipeline behavior,
- state changes are explicit,
- the system can be validated and regression-tested.

### Physics-inspired numerical safeguards

Instead of hard clipping, the system uses the **Heisenberg Soft Clip** operator (`mathematics/safe_operations.py`) to keep observables stable without discontinuities.

### LLMs are optional—and *not* the reasoning engine

The LLM integration (`ciel/hf_backends.py`, `ciel/llm_registry.py`) is treated as:

- a linguistic interpreter,
- a controlled expression layer,
- an analysis/validation assistant.

If transformers / torch are not installed, the system degrades gracefully to deterministic stub backends.

---

## Breakthrough modules & structures (what actually matters)

Below are the key subsystems that define CIEL/Ω as an engineering platform.

### 1) `CielEngine` — the orchestrated core

`ciel/engine.py` exposes `CielEngine.step(...)` and `CielEngine.interact(...)`.

It composes:

- intention → wave kernel → memory TMP → cognition → emotion → optional language layer

### 2) Fourier Wave Consciousness Kernel (12D)

`ciel_wave/fourier_kernel.py` provides:

- `SpectralWaveField12D` (fast synthesis)
- `FourierWaveConsciousnessKernel12D` (snapshot metrics: bands, coherence/entropy/purity, resonance tensor, soul measure)

This creates a stable, measurable internal state representation rather than a purely textual “thought stream”.

### 3) The Information Flow Pipeline

`integration/information_flow.py` builds a deterministic pipeline:

- EEG-like signal → intention → emotion mapping → soul invariant → persistence

It is a testable and auditable “sensor-to-memory” path.

### 4) Soul Invariant (σ)

`fields/soul_invariant.py` computes a spectral invariant over a 2D field.

In practice it acts as a stable quantitative anchor for:

- coherence metrics
- ethical gating
- system introspection

### 5) Memory architecture with vendor profiles

Memory is modular by design:

- `core/memory/vendor/repo` (lightweight)
- `core/memory/vendor/pro` (SQLite + optional HDF5)
- `core/memory/vendor/ultimate` (adds audit logging and stronger operational structure)

Vendor selection is controlled via `CIEL_MEM_VENDOR`.

### 6) Braid subsystem (topological loops, scars, glyphs)

`core/braid/` introduces a structured representation of contradictions and resolutions:

- **loops** (intent execution cycles)
- **scars** (residual contradictions with a curvature budget)
- **glyphs & rituals** (operators applied to braid memory)

This is a compact, engineering-friendly model for “structured cognition under constraints”.

---

## What CIEL/Ω can revolutionize

CIEL/Ω is positioned to transform domains where *trust* is the bottleneck.

### Government & public institutions

- auditable decision-support pipelines
- stable behavioral constraints
- reproducible state transitions (no “mood drift”)

### Medicine & clinical research (R&D context)

- deterministic pipelines for signal processing, feature extraction and memory persistence
- ethics-first gating before any downstream “recommendation” layer

Note: this repository is **research software** and is not a certified medical device.

### Pharma & biotech

- disciplined model-driven experimentation
- consistent simulation kernels and invariant metrics
- traceable memory/audit logs (vendor ultimate)

### Education

- interactive, testable modules for wave-field simulation and cognition/affect modeling
- safer LLM usage as an *interface*, not an authority

### Business & strategic operations

- stable, bounded decision assistance
- measurable coherence and risk signals
- audit-friendly outputs and structured memory

### AI Safety & trustworthy automation

- “hard-stop ethics” as runtime policy, not as marketing
- deterministic regression tests as a first-class feature

---

## System specifications & requirements

### Supported platforms

- Linux (recommended)
- macOS
- Windows

### Core software requirements

- Python 3.10+ recommended
- Minimal dependencies (as shipped):
  - `numpy`, `scipy`, `matplotlib`, `networkx`, `sympy`, `pandas`

Optional dependencies (only if you enable related modules):

- **LLM backends**: `transformers` (+ typically `torch`)
- **Ultimate/Pro memory features**: `h5py` (true HDF5), `streamlit` (dashboard)
- **GUI client** (`CLI.py`): PyQt5 + audio/report packages (see `hints.md`)

### Hardware guidelines

Minimum (core deterministic pipeline):

- CPU: 2+ cores
- RAM: 4 GB
- Disk: 1 GB free (more if you persist memory histories)

Recommended (development + experiments):

- CPU: 6–12 cores
- RAM: 16–32 GB

Optional (local LLM inference):

- NVIDIA GPU recommended
- VRAM: typically 12–24 GB depending on model size and quantization

---

## Getting started

- Run smoke test: `python scripts/smoke_test.py`
- Run CLI engine: `python -m ciel`
- If you use the GUI client, see `run_gui.sh` and ensure GUI dependencies are installed.

---

## License

CIEL Research Non-Commercial License v1.1  
SPDX-License-Identifier: CIEL-Research-NonCommercial-1.1

---

## Citation

```
A. Lipa, S. Sakpal, M. Kamecka, U. Ahmad (2025). CIEL/Ω — General Quantum Consciousness System.
https://github.com/AdrianLipa90/CIEL-Omega-General-Quantum-Consciousness/
```

---

## Contact

See `LICENSE` file for contact email.
