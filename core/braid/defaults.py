from __future__ import annotations

import math
from typing import TYPE_CHECKING

from .glyphs import Glyph, GlyphEngine, Ritual, RitualEngine
from .memory import BraidMemory
from .phase_field import PhaseField
from .runtime import BraidRuntime
from .scars import ScarRegistry
from .scheduler import Scheduler

if TYPE_CHECKING:  # pragma: no cover
    from .loops import Loop


def glyph_bind(loop: "Loop", memory: BraidMemory) -> None:
    weight = max(0.1, min(1.0, loop.contradiction))
    content = {
        "loop_id": loop.loop_id,
        "type": "bind",
        "contradiction": loop.contradiction,
    }
    memory.add(content=content, phase=loop.phase, weight=weight)


def glyph_reflect(loop: "Loop", memory: BraidMemory) -> None:
    weight = max(0.1, min(1.0, loop.contradiction))
    content = {
        "loop_id": loop.loop_id,
        "type": "reflect",
        "contradiction": loop.contradiction,
    }
    memory.add(content=content, phase=-loop.phase, weight=weight)


def ritual_stabilize(loop: "Loop", memory: BraidMemory) -> None:
    for unit in memory.units:
        alpha = 0.05
        delta = (loop.phase - unit.phase + math.pi) % (2.0 * math.pi) - math.pi
        unit.phase = (unit.phase + alpha * delta) % (2.0 * math.pi)


def make_default_runtime() -> BraidRuntime:
    memory = BraidMemory()
    scars = ScarRegistry(scar_budget=1.0)
    glyph_engine = GlyphEngine()
    ritual_engine = RitualEngine()
    phase_field = PhaseField(global_phase=0.0, omega=0.0)
    scheduler = Scheduler()

    glyph_engine.register(
        Glyph(
            name="bind",
            operator=glyph_bind,
            domain="generic",
            risk_level="low",
            description="Wpisuje sprzeczność jako nowy węzeł pamięci.",
        )
    )
    glyph_engine.register(
        Glyph(
            name="reflect",
            operator=glyph_reflect,
            domain="generic",
            risk_level="medium",
            description="Tworzy odbicie fazowe sprzeczności.",
        )
    )

    ritual_engine.register(
        Ritual(
            name="stabilize",
            operator=ritual_stabilize,
            kind="stabilizing",
            description="Delikatnie synchronizuje fazy w stronę nowej pętli.",
        )
    )

    return BraidRuntime(
        memory=memory,
        scars=scars,
        glyph_engine=glyph_engine,
        ritual_engine=ritual_engine,
        phase_field=phase_field,
        scheduler=scheduler,
    )
