from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

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
            text_summary.append(f'{node.name} × {w:.2f}')
        coherence = float(np.mean(weights))
        sigma_mod = float(np.mean(self.sigma_field)) if self.sigma_field is not None else 1.0
        color_mix = min(1.0, coherence * sigma_mod)
        return {'coherence': coherence, 'color_mix': color_mix, 'summary': ' | '.join(text_summary)}