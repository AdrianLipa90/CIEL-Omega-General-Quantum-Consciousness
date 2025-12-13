"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Interpret glyphs into symbolic operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(slots=True)
class GlyphNode:
    id: str
    name: str
    code: str
    field_key: str
    operator_signature: str
    active: bool = False

    def execute(self) -> str:
        self.active = True
        return f"[{self.id}] {self.name} executed by {self.operator_signature}\n→ {self.code}"

    def transfer_to(self, new_operator: str) -> None:
        self.operator_signature = new_operator
        self.active = False


@dataclass(slots=True)
class GlyphNodeInterpreter:
    registry: Dict[str, GlyphNode] = field(default_factory=dict)

    def interpret(self, glyph: dict[str, object]) -> str:
        name = glyph.get("name", "unknown")
        strokes = glyph.get("strokes", 0)
        return f"{name}:{strokes}"

    def register(self, node: GlyphNode) -> None:
        self.registry[node.id] = node

    def execute_sequence(self, ids: List[str]) -> List[str]:
        outputs: List[str] = []
        for gid in ids:
            node = self.registry.get(gid)
            if node is not None:
                outputs.append(node.execute())
        return outputs


__all__ = ["GlyphNode", "GlyphNodeInterpreter"]
