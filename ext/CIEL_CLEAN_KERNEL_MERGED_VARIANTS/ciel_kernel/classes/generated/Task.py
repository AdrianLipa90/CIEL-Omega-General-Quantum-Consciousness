import numpy as np
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

class Task:
    """Single subtask in the mission to heal the planet"""
    id: str
    name: str
    description: str
    deadline: Optional[str]
    dependencies: List[str]
    progress: float
    status: str
    assigned_to: str

    def to_dict(self) -> Dict:
        return asdict(self)