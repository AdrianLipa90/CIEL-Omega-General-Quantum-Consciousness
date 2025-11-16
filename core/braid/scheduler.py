from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .loops import Loop


@dataclass
class Scheduler:
    queue: List[Loop] = field(default_factory=list)

    def add_loop(self, loop: Loop) -> None:
        self.queue.append(loop)

    def next_batch(self, max_loops: int = 4) -> List[Loop]:
        self.queue.sort(key=lambda loop: loop.curvature)
        batch = self.queue[:max_loops]
        self.queue = self.queue[max_loops:]
        return batch
