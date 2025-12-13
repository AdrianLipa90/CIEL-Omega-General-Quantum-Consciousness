from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional
import numpy as np
import threading, queue, time

def _demo():
    eeg = EEGProcessor()
    vm = VoiceMemoryUI()
    sig = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 256)) + 0.3 * np.random.randn(256)
    print('EEG bands:', eeg.analyze(sig))

    def fake_step():
        val = np.random.rand()
        vm.add_entry(f'Step value {val:.3f}', mood='positive' if val > 0.5 else 'neutral')
        return {'value': val}
    ctl = RealTimeController(step_fn=fake_step, on_step=lambda i, d: print(f'Step {i}: {d}'), steps=5)
    ctl.start()
    ctl._thread.join()
    vm.display()