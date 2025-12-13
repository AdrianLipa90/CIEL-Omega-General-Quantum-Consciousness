from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional
import numpy as np
import threading, queue, time

class RealTimeController:
    step_fn: Callable[[], Dict[str, float]]
    on_step: Optional[Callable[[int, Dict[str, float]], None]] = None
    interval: float = 0.1
    steps: int = 100
    _running: bool = field(default=False, init=False)
    _thread: Optional[threading.Thread] = field(default=None, init=False)

    def _loop(self):
        for i in range(self.steps):
            if not self._running:
                break
            data = self.step_fn()
            if self.on_step:
                self.on_step(i, data)
            time.sleep(self.interval)
        self._running = False

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)