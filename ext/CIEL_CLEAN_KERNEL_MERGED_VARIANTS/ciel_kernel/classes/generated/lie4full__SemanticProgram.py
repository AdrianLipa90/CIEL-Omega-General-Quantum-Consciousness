import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings

class SemanticProgram:
    intent: str
    emotions: Emotions = field(default_factory=Emotions)
    input_value: complex = complex(1.0, 0.0)
    rules: List[str] = field(default_factory=list)
    pipeline: List[Tuple[str, Dict[str, Any]]] = field(default_factory=list)
    config: SemanticConfig = field(default_factory=SemanticConfig)