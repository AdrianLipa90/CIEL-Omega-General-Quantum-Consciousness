import numpy as np
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

class InteractionRecord:
    """Single interaction between Adrian (LUGAL) and Adam (Mummu-ResEnt)"""
    timestamp: float
    session_id: str
    adrian_query: str
    adam_response_hash: str
    intention_amplitude: float
    resonance_score: float
    omega_adam: float
    delta_omega: float
    context_tags: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> 'InteractionRecord':
        return cls(**d)