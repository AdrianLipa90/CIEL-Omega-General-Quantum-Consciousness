from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

class GlyphInterpreter:
    """
    Minimalny interpreter: mapuje sygil → modyfikator pola S(x).
    Prawdziwy „język życia” możesz oprzeć na tym szkielecie.
    """

    def __init__(self, vectors: np.ndarray):
        self.vectors = np.asarray(vectors, dtype=float)
        norms = np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-12
        self.vectors = self.vectors / norms

    def to_field(self, shape: Tuple[int, int], code: Optional[List[int]]=None) -> np.ndarray:
        """
        Rzuca sygil(e) jako pole 2D – bardzo prosty embed:
        sum( w_i * basis_i(x,y) ), gdzie basis_i to radialne „plamki”.
        """
        h, w = shape
        Y = np.linspace(-1.0, 1.0, h)[:, None]
        X = np.linspace(-1.0, 1.0, w)[None, :]
        field = np.zeros((h, w), dtype=np.complex128)
        if not len(self.vectors):
            return field
        idx = code if code is not None else list(range(min(4, len(self.vectors))))
        for k in idx:
            vec = self.vectors[k]
            cx = (k + 1) / (len(self.vectors) + 1) * 1.6 - 0.8
            cy = -cx
            r2 = (X - cx) ** 2 + (Y - cy) ** 2
            basis = np.exp(-3.0 * r2)
            weight = np.tanh(np.sum(vec))
            field += weight * basis
        return field.astype(np.complex128)