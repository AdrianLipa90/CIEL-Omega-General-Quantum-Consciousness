from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import cmath
import math
import uuid

from .glyphs import GlyphEngine, RitualEngine
from .loops import Loop, LoopType
from .memory import BraidMemory
from .phase_field import PhaseField
from .scheduler import Scheduler
from .scars import ScarRegistry


@dataclass
class BraidRuntime:
    memory: BraidMemory
    scars: ScarRegistry
    glyph_engine: GlyphEngine
    ritual_engine: RitualEngine
    phase_field: PhaseField
    scheduler: Scheduler

    def detect_contradiction(self, intention: complex) -> float:
        mem_phasor = self.memory.mean_phasor()
        return abs(mem_phasor - intention)

    def estimate_curvature(self, contradiction: float) -> float:
        return contradiction

    def build_loop(
        self,
        intention: complex,
        domain: str = "generic",
        loop_type: LoopType = LoopType.LB,
    ) -> Loop:
        contradiction = self.detect_contradiction(intention)
        curvature = self.estimate_curvature(contradiction)
        phase = math.atan2(intention.imag, intention.real)

        glyph = self.glyph_engine.choose_for(contradiction, domain=domain)
        ritual = self.ritual_engine.choose_for(contradiction)

        loop = Loop(
            loop_id=str(uuid.uuid4()),
            loop_type=loop_type,
            contradiction=contradiction,
            phase=phase,
            glyph=glyph,
            ritual=ritual,
            curvature=curvature,
        )
        return loop

    def execute_loop(self, loop: Loop) -> bool:
        if not self.scars.can_execute(loop.curvature):
            self.scars.register_scar(
                contradiction=loop.contradiction,
                glyph_name=loop.glyph.name,
                curvature=loop.curvature,
                phase=loop.phase,
                scar_type="fracture",
                delta_memory_summary="blocked_by_budget",
            )
            loop.closed = False
            return False

        if loop.ritual is not None:
            loop.ritual.operator(loop, self.memory)

        loop.glyph.operator(loop, self.memory)
        loop.closed = True

        post_C = self.memory.coherence()
        post_P = loop.contradiction
        post_E = post_C - post_P
        loop.meta["post_C"] = post_C
        loop.meta["post_P"] = post_P
        loop.meta["post_E"] = post_E

        self.scars.register_scar(
            contradiction=loop.contradiction,
            glyph_name=loop.glyph.name,
            curvature=-abs(loop.curvature),
            phase=loop.phase,
            scar_type="resolution",
            delta_memory_summary="loop_resolved",
        )

        return True

    def submit_intention(
        self,
        magnitude: float,
        phase_offset: float,
        domain: str = "generic",
        loop_type: LoopType = LoopType.LB,
    ) -> Loop:
        phi = self.phase_field.current() + phase_offset
        intention = magnitude * cmath.exp(1j * phi)
        loop = self.build_loop(intention=intention, domain=domain, loop_type=loop_type)
        self.scheduler.add_loop(loop)
        return loop

    def step(self, max_loops: int = 4) -> List[Tuple[Loop, bool]]:
        batch = self.scheduler.next_batch(max_loops=max_loops)
        results: List[Tuple[Loop, bool]] = []
        for loop in batch:
            success = self.execute_loop(loop)
            results.append((loop, success))
        return results
