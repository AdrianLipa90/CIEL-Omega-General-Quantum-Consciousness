from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

class GlyphNodeInterpreter:
    """Interpreter sekwencji glyphów (BraidOS DSL)."""
    registry: Dict[str, GlyphNode] = field(default_factory=dict)

    def register(self, node: GlyphNode):
        self.registry[node.id] = node

    def execute_sequence(self, ids: List[str]) -> List[str]:
        """Wykonuje sekwencję glyphów."""
        outputs = []
        for gid in ids:
            node = self.registry.get(gid)
            if node:
                outputs.append(node.execute())
        return outputs