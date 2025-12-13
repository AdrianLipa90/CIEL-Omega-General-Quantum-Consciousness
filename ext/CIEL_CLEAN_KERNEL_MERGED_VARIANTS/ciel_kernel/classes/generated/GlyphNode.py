from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

class GlyphNode:
    id: str
    name: str
    code: str
    field_key: str
    operator_signature: str
    active: bool = False

    def execute(self) -> str:
        self.active = True
        out = f'[{self.id}] {self.name} executed by {self.operator_signature}\n→ {self.code}'
        print(out)
        return out

    def transfer_to(self, new_operator: str):
        self.operator_signature = new_operator
        self.active = False