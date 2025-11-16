from __future__ import annotations

from dataclasses import dataclass, field
import math
import time


@dataclass
class PhaseField:
    global_phase: float = 0.0
    omega: float = 0.0
    last_update: float = field(default_factory=time.time)

    def advance(self) -> None:
        current_time = time.time()
        delta = current_time - self.last_update
        self.global_phase = (self.global_phase + self.omega * delta) % (2.0 * math.pi)
        self.last_update = current_time

    def current(self) -> float:
        self.advance()
        return self.global_phase
