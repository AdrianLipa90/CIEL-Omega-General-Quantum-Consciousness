import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings

class Emotions:
    love: float = 0.0
    joy: float = 0.0
    fear: float = 0.0
    anger: float = 0.0
    sadness: float = 0.0
    peace: float = 0.0

    def normalized(self) -> 'Emotions':
        vals = [self.love, self.joy, self.fear, self.anger, self.sadness, self.peace]
        total = sum((max(0.0, v) for v in vals))
        if total <= 1e-12:
            return Emotions()
        scale = 1.0 / total
        return Emotions(love=max(0.0, self.love) * scale, joy=max(0.0, self.joy) * scale, fear=max(0.0, self.fear) * scale, anger=max(0.0, self.anger) * scale, sadness=max(0.0, self.sadness) * scale, peace=max(0.0, self.peace) * scale)

    def as_dict(self) -> Dict[str, float]:
        return {'love': self.love, 'joy': self.joy, 'fear': self.fear, 'anger': self.anger, 'sadness': self.sadness, 'peace': self.peace}