import numpy as np
from kernels.adapters.wave_adapter import capture_wave
amp = np.random.rand(64,64).astype("float32")
phase = np.random.rand(64,64).astype("float32")
refs = capture_wave(amp, phase, attrs={"grid":"64x64","units":"arb"})
print(refs)
