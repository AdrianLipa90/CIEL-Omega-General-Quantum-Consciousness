# -*- coding: utf-8 -*-
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

CIEL/0 – Batch8 Patch (Symbolic Kit)
Integruje:
- CVOSDatasetLoader → wczytywanie danych JSON/TXT (sigile, glyphy)
- GlyphNodeInterpreter → wykonawca sekwencji symbolicznych (język BraidOS)
- GlyphPipeline → prosty mechanizm łączenia wielu glyphów w łańcuch
- SymbolicBridge → glue między ColorOS, Σ i glyphami

Nie dubluje niczego z wcześniejszych patchy.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

# =======================================================================
# 1️⃣ CVOSDatasetLoader – ładowanie sygli i glyphów z plików JSON/TXT
# =======================================================================
@dataclass
class CVOSDatasetLoader:
    """Loader datasetów CVOS (sigile, glyphy, Z-serie)."""
    base_path: str = "."

    def load_json(self, filename: str) -> List[Dict[str, Any]]:
        """Ładuje sygle CVOS (JSON)."""
        path = os.path.join(self.base_path, filename)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
        if "sigils" in data:
            return data["sigils"]
        elif isinstance(data, list):
            return data
        else:
            return [data]

    def load_txt(self, filename: str) -> List[Dict[str, Any]]:
        """Ładuje pliki Z-serii TXT (np. cvos.glyphs.Z5)."""
        path = os.path.join(self.base_path, filename)
        entries = []
        current = {}
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip(), v.strip()
                    if k in current:
                        # nowy rekord
                        entries.append(current)
                        current = {}
                    current[k] = v
            if current:
                entries.append(current)
        return entries

# =======================================================================
# 2️⃣ GlyphNodeInterpreter – wykonawca DSL glyphów
# =======================================================================
@dataclass
class GlyphNode:
    id: str
    name: str
    code: str
    field_key: str
    operator_signature: str
    active: bool = False

    def execute(self) -> str:
        self.active = True
        out = f"[{self.id}] {self.name} executed by {self.operator_signature}\n→ {self.code}"
        print(out)
        return out

    def transfer_to(self, new_operator: str):
        self.operator_signature = new_operator
        self.active = False

@dataclass
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

# =======================================================================
# 3️⃣ GlyphPipeline – łączenie wielu glyphów (rytmy, kolory, Σ)
# =======================================================================
@dataclass
class GlyphPipeline:
    """Łańcuch operacji glyphicznych."""
    nodes: List[GlyphNode]
    color_weights: Optional[List[float]] = None
    sigma_field: Optional[np.ndarray] = None

    def combine(self) -> Dict[str, Any]:
        """Łączy efekty glyphów (symbolicznie: średnia ważona, Σ jako modulacja)."""
        weights = np.ones(len(self.nodes)) if self.color_weights is None else np.array(self.color_weights)
        weights = weights / (np.sum(weights) + 1e-12)
        text_summary = []
        for w, node in zip(weights, self.nodes):
            text_summary.append(f"{node.name} × {w:.2f}")
        coherence = float(np.mean(weights))
        sigma_mod = float(np.mean(self.sigma_field)) if self.sigma_field is not None else 1.0
        color_mix = min(1.0, coherence * sigma_mod)
        return {"coherence": coherence, "color_mix": color_mix, "summary": " | ".join(text_summary)}

# =======================================================================
# 4️⃣ SymbolicBridge – łącze ColorOS ↔ Σ ↔ Glyph
# =======================================================================
@dataclass
class SymbolicBridge:
    """Integruje glyphy z ColorOS i Σ (no-FFT)."""
    sigma_scalar: float
    palette: Dict[str, Tuple[float, float, float]] = field(default_factory=lambda: {
        "SOUL_BLUE": (0.2, 0.4, 0.9),
        "INTENTION_GOLD": (0.95, 0.8, 0.2),
        "ETHICS_WHITE": (1.0, 1.0, 0.95),
        "WARNING_RED": (0.9, 0.2, 0.2),
        "BALANCE_GREEN": (0.3, 0.9, 0.5)
    })

    def glyph_color(self, coherence: float) -> Tuple[float, float, float]:
        """Łączy Σ z koherencją glyphu i zwraca kolor RGB."""
        val = np.clip(coherence * self.sigma_scalar, 0.0, 1.0)
        if val < 0.3:
            base = np.array(self.palette["WARNING_RED"])
        elif val < 0.7:
            base = np.array(self.palette["INTENTION_GOLD"])
        else:
            base = np.array(self.palette["ETHICS_WHITE"])
        return tuple(base * val + (1 - val) * np.array(self.palette["SOUL_BLUE"]))

# =======================================================================
# 5️⃣ Mini-demo – symboliczny pipeline (bez GUI)
# =======================================================================
def _demo():
    # loader przykładowych danych
    loader = CVOSDatasetLoader(base_path="/mnt/data/CIEL_extracted/CIEL")
    try:
        sigils = loader.load_json("CVOS_GliphSigils_MariaKamecka.json")
        print(f"Loaded {len(sigils)} sigils from CVOS.")
    except Exception as e:
        print("Could not load CVOS dataset:", e)
        sigils = []

    # tworzymy kilka node'ów ręcznie
    n1 = GlyphNode(id="GLIF_GEN.01C", name="Glyph of the First Symphony",
                   code="intent.sound[α₁] >> field.init(resonance)", field_key="CVOS::GENESIS_01", operator_signature="INT::LIPA.001")
    n2 = GlyphNode(id="GLIF_HEL.04C", name="Glyph of the Double Helix",
                   code="intent.duality[Ω₂] >> chain.twist(A∩T/G∩C)", field_key="CVOS::HELIX", operator_signature="INT::LIPA.001")
    interp = GlyphNodeInterpreter()
    interp.register(n1); interp.register(n2)
    interp.execute_sequence(["GLIF_GEN.01C", "GLIF_HEL.04C"])

    # pipeline z Σ i kolorystyką
    pipeline = GlyphPipeline(nodes=[n1, n2], color_weights=[0.6, 0.4], sigma_field=np.random.rand(64, 64))
    result = pipeline.combine()
    bridge = SymbolicBridge(sigma_scalar=result["coherence"])
    color = bridge.glyph_color(result["coherence"])

    print("Pipeline summary:", result["summary"])
    print("Coherence:", round(result["coherence"], 4), "→ Color:", color)

if __name__ == "__main__":
    _demo()