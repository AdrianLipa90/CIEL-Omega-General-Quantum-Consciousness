import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings

class SCLParser:

    def parse(self, text: str) -> SemanticProgram:
        lines = text.split('\n')
        intent = ''
        emotions = Emotions()
        for line in lines:
            line = line.strip()
            if line.startswith('INTENT:'):
                intent = line.replace('INTENT:', '').strip().strip('"')
            elif '=' in line:
                for emotion in ['love', 'joy', 'fear', 'anger', 'sadness', 'peace']:
                    if emotion in line:
                        try:
                            value = float(line.split('=')[1].strip())
                            setattr(emotions, emotion, value)
                        except:
                            pass
        return SemanticProgram(intent=intent, emotions=emotions.normalized())