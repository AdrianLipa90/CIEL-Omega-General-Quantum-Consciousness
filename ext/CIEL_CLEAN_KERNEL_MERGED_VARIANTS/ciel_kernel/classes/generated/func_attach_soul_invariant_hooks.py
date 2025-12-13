from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

def attach_soul_invariant_hooks(kernel: KernelSpec) -> SoulInvariantOperator:
    """
    Zwraca operator Σ i niczego nie „patrzy w środek” kernela.
    Wołasz ręcznie w swojej pętli, jeśli chcesz.
    """
    return SoulInvariantOperator()