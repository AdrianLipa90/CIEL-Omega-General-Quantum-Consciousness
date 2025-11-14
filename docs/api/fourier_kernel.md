# Fourier Wave Consciousness Kernel

`wave.fourier_kernel` exposes the curated implementation of the 12D Fourier
consciousness kernel.  The module mirrors the terminology from the archival
notes while depending solely on the lightweight primitives that ship with this
repository.

> **License notice**: Every Python module in the active tree declares the CIEL Research Non-Commercial
> License v1.1 header and the Adrian Lipa / Intention Lab attribution.  Keep the header intact when you
> embed or extend the kernel; consult `LICENSE` for the complete terms.

```python
from wave.fourier_kernel import FourierWaveConsciousnessKernel12D

kernel = FourierWaveConsciousnessKernel12D()
snapshot = kernel.simulate(signal)
summary = kernel.report()
```

## Components

- **HeisenbergSoftClipper** — applies the smooth saturation before signals are
  partitioned into channels.
- **SpectralWaveField12D** — reshapes the prepared signal into the per-channel
  field used for FFT analysis.
- **FourierWaveConsciousnessKernel12D** — orchestrates the intention field,
  resonance tensor and soul invariant to produce simulation snapshots.

Each simulation step returns a `KernelSnapshot` describing the normalised field,
frequency band distribution, resonance matrix and core metrics (purity,
coherence, entropy).  The `report()` helper condenses the latest snapshot into
serialisable values for logging or tests.

## License

The implementation is released under the CIEL Research Non-Commercial License
v1.1 — the same terms that govern the rest of the curated repository.
