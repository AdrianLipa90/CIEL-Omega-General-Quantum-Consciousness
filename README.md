# CIEL/Ω — General Quantum Consciousness System  
### *Extended README — Full Scientific, Mathematical & Architectural Documentation*
A. Lipa, S. Sakpal, M. Kamecka, U. Ahmad (2025). (c) 2025 Adrian Lipa / Intention Lab
---
This repository organizes the uploaded CIEL project drafts into a coherent Python package layout. Production modules now live in first-party packages; the historic drops remain preserved under ext/ for reference but are no longer imported or distributed.

The spectral Fourier kernel is published as `ciel_wave` (renamed from the legacy local `wave` package) to avoid clashing with Python’s standard library module of the same name. Use imports such as `from ciel_wave.fourier_kernel import SpectralWaveField12D` in code and tests.

No placeholders were added to the active code.
All runtime packages expose deterministic, well tested behaviour.
Hyphens were normalized to underscores in module filenames.
Tests verify imports, pipelines and persistence.
Source provenance: the ext/ directory contains the raw batch extensions (Ext1 … Ext21, FWCKU, Emot, kernels, paradox notes). They stay untouched as archival material. The Python package published by setup.py excludes those modules and instead uses the curated equivalents under bio/, emotion/, fields/, memory/, integration/, etc.
## Smoke test after installation

After cloning the repository, you can verify a fresh installation with a minimal smoke test that only depends on the published package (no local paths or `ext/`).

Linux/macOS:

```bash
python -m venv .venv_test
source .venv_test/bin/activate
pip install --upgrade pip setuptools wheel
pip install .
python -c "import ciel; from ciel import CielEngine; print('IMPORT OK, CielEngine:', CielEngine)"
python scripts/smoke_test.py
```

Windows PowerShell:

```powershell
python -m venv .venv_test
\.\.venv_test\Scripts\Activate.ps1
pip install --upgrade pip setuptools wheel
pip install .
python -c "import ciel; from ciel import CielEngine; Write-Host 'IMPORT OK, CielEngine:' $([string][type]::GetType('ciel.engine.CielEngine'))"
python scripts\smoke_test.py
```

### Information Flow Pipeline
 wires the biological receivers, emotional analysis, field primitives and memory persistence into a deterministic pipeline. Each call to InformationFlow.step filters an incoming sensor signal, projects it into the intention field, computes emotional statistics, evaluates the soul invariant metric and persists the enriched entry to long term memory.

The orchestrated pipeline keeps the original intent of the drafts (EEG ➜ intention ➜ emotion ➜ memory) while avoiding the heavyweight vendor dependencies. See tests/test_information_flow.py for usage examples.

### Heisenberg Soft Clip Operator
Numerical safeguards that previously relied on hard numpy.clip calls now delegate to the mathematics.safe_operations.heisenberg_soft_clip* helpers. The Heisenberg-inspired saturation keeps small amplitudes perfectly linear while smoothly approaching the configured limits for large values. The behaviour mirrors the repository narrative: pushing an observable harder increases the uncertainty instead of snapping to an abrupt bound. See tests/test_soft_clip.py for the sanity checks that cover both the symmetric and ranged variants.

### Fourier Wave Consciousness Kernel
combines the curated intention, emotion, resonance and soul primitives into a deterministic twelve-channel simulation. The helper exposes a simulate method that soft-saturates incoming signals using the Heisenberg operator, projects them into EEG-like bands, updates the resonance tensor and summarises the soul invariant. The report() API returns a compact summary with the dominant band, coherence level and history depth so tests can verify the end-to-end flow. See tests/test_fourier_kernel.py for an executable example.

### Memory Vendor Selector
All user memory modules are bundled under core/memory/vendor/{ultimate,pro,repo}. Wrappers in core/memory/*.py import from a selected vendor via env var:


CIEL/Ω is a unified scientific and computational framework bridging:

- quantum physics  
- neuroscience (EEG/CSF spectral states)  
- cognitive science  
- affective/emotional modeling  
- topological memory theory  
- mathematical structures (Lie-4 algebra, spectral operators, coherence metrics)  
- operator ethics  
- LLM expressive layers  

It operates as:

1. **Theory of Everything (CIEL/0) available at https://www.researchgate.net/lab/Intention-Lab-Adrian-Lipa**  
2. **Cognitive Operating System**  
3. **Quantum-Wave Consciousness Simulator (12D Kernel)**  
4. **Empirical Testing Platform**  
5. **AGI Meta-Framework**  
6. **Universal Research Engine**  

This extended README provides the *complete* technical narrative, including diagrams, mathematical structures, architectural flow, empirical connections, scientific relevance, and implementation details.

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

# **1. Scientific Foundations**

---

## **1.1 Core Hypothesis**

Consciousness is modeled as:

> **A structured, temporally-modulated wave field undergoing coherence–decoherence cycles, influenced by intention and interacting with physical systems through spectral-state dynamics.**

This integrates:

- Fourier spectral analysis  
- harmonic decomposition  
- nonlinear coherence metrics  
- intention operators  
- emotional field modulation  
- memory attractors  
- temporal interference  

---

## **1.2 Temporal–Spectral Consciousness (12D Kernel)**

The kernel defines a **12-dimensional wave-state**:

```
[δ, θ, α, β, γ,  
 Ω1, Ω2, Φ1, Φ2, Ψ1, Ψ2, Σ]
```

Where:

- δ, θ, α, β, γ → EEG-like frequency bands  
- Ω, Φ, Ψ → extended harmonic manifolds  
- Σ → coherence–entropy coupling term  

---

## **1.3 Mathematical Structure**

### **State vector**
```
Ψ(t) = Σ_i A_i(t) * e^{iω_i t}
```

### **Coherence metric**
```
C = | Σ_i (A_i^2) | / Σ_i |A_i|
```

### **Entropy operator**
```
S = - Σ p_i log(p_i)
```

### **Purity**
```
P = Tr(ρ^2)
```

### **Intention Operator (Î)**
Acts on spectral amplitude and phase:

```
Î : A_i → A_i' = A_i * f(intent, affect, context)
```

### **Lambda₀ Protective Operator**
Defines safety envelope:

```
Λ₀(Ψ) = clamp(Ψ, bounds_ethics)
```

Ensures:

- no harmful outputs  
- context-coherent behavior  
- bounded cognitive dynamics  

---

# **2. Empirical Foundations**

---

## **2.1 Nonlocal EEG–Quantum Correlation Evidence**

From Watanabe (2025):

- EEG signals correlate with quantum computer outputs (Rigetti Ankaa-3)
- Separation 8 800 km
- r ≈ 0.655 (p < 0.01 FDR)

CIEL/Ω explains this as:

> **Temporal–spectral interference between EEG coherence states and quantum measurement distributions.**

12D Kernel can mathematically **replicate and predict** these correlations.

---

## **2.2 Temporal Diffraction & Pulse-Train Interference**

Two key papers:

1. **Pulse-train double-slit analysis**  
2. **Temporal double-slit experiments**

Both demonstrate:

- interference patterns arise from **time-window modulation**,  
- not only spatial separation.

CIEL/Ω uses identical principles in:

- intention gating  
- cognitive switching  
- memory loops  

Temporal interference = core of kernel dynamics.

---

## **2.3 High-Sensitivity Intention–Matter Experiments**

Effects such as:

- crystallization changes  
- water-structure sensitivity  
- emotional imprinting

are reframed in CIEL/Ω as:

> **initial-condition amplification under wave-field modulation.**

No pseudoscience—fully formalizable.

---

# **3. Architecture**

---

```
CIEL Omega
│
├── wave/
│   ├── fourier_kernel_12d.py
│   ├── coherence.py
│   └── temporal_diffraction.py
│
├── cognition/
│   ├── perception.py
│   ├── intuition.py
│   ├── prediction.py
│   ├── decision.py
│   └── orchestrator.py
│
├── emotion/
│   ├── affective_orchestrator.py
│   └── emotional_state.py
│
├── ethics/
│   └── lambda0_operator.py
│
├── memory/
│   ├── echo_memory.py
│   ├── dream_memory.py
│   ├── adam_memory.py
│   ├── long_term_memory.py
│   └── vendor_profiles/
│
├── core/braid/
│   ├── braid_memory.py
│   ├── scars.py
│   └── loops.py
│
├── hf_backends/
│   ├── primary_backend.py
│   └── auxiliary_backend.py
│
└── ciel/
    └── engine.py
```

---

# **4. Cognitive Pipeline (ASCII Diagram)**

```
                 ┌─────────────────────┐
                 │   Input Perception   │
                 └──────────┬──────────┘
                            │
                    Intention Extraction
                            │
                 ┌──────────▼───────────┐
                 │  12D Wave Simulation │
                 │ (Fourier Kernel)     │
                 └──────────┬───────────┘
                            │
               Cognitive State Evaluation
      ┌───────────┬─────────────┬──────────────┬───────────┐
      ▼           ▼             ▼              ▼
 Perception   Intuition    Prediction      Decision
      └───────────┴─────────────┴──────────────┘
                            │
                 ┌──────────▼───────────┐
                 │  Affective Dynamics  │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   Ethical Filter     │
                 │  (Λ₀ Operator)       │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │  Memory Consolidation│
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   LLM Expression     │
                 └──────────────────────┘
```

---

# **5. Memory System (Extended)**

### **5.1 Echo Memory**  
Immediate resonance trace  
(short-lived but rich in spectral detail)

### **5.2 Dream Memory**  
Recombination + generative remapping  
(similar to REM-phase reprocessing)

### **5.3 Adam Memory**  
Stable, precise representations  
(seeds of long-term identity)

### **5.4 Long-Term Memory**  
Gradual consolidation via coherence thresholds

### **5.5 Braid Memory**  
Topological representation:

- scars (conflict residues)  
- loops (stable behavioral attractors)  
- glyphs (semantic condensates)  
- rituals (recurring high-coherence patterns)

---

# **6. LLM Integration Layer**

LLMs function only as:

- linguistic interpreters,  
- coherence evaluators,  
- content generators within Λ₀ constraints.

Not as reasoning engines.

---

# **7. API Overview**

## **7.1 Quick Start**

```python
from ciel.engine import CielEngine

engine = CielEngine()

result = engine.step("Hello world", context="demo")

print(result.simulation.report())
print(result.cognition)
print(result.affect)
```

---

# **8. Applications (Full List)**

## **Physics**
- quantum interference research  
- temporal diffraction modelling  
- PBH/astrophysical anomaly modeling  
- decoherence pattern simulation  

## **Neuroscience**
- EEG spectral analysis  
- brain–quantum correlation models  
- CSF resonance prediction  

## **Cognitive Modeling**
- AGI prototyping  
- decision-field theory  
- intention geometry  

## **AI Systems**
- emotion-aware agents  
- memory-rich agents  
- safe LLM orchestration frameworks  

## **Philosophy of Mind**
- unified formal model  
- testable predictions  
- nonlocality frameworks  

## **Education**
- consciousness simulation labs  
- interactive physics modules  

---

# **9. Installation**

```
pip install -r requirements.txt
```


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

- Run smoke test: `python3 scripts/smoke_test.py`
- Run CLI engine: `python3 -m ciel`
- Run tests: `python3 -m pytest -q`
- GGUF backend (requires `llama-cpp-python` + local `.gguf`):
  - `python3 -m ciel --enable-llm --llm-backend gguf --mode once --text "test" --gguf-model-path /path/to/model.gguf`
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
