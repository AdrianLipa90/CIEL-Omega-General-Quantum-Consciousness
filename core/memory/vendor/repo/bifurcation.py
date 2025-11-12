from enum import Enum
from .weighting import decision_thresholds

class Path(Enum):
    TMP='tmp'; OUT='out'; MEM='mem'

def decide_branch(weight: float):
    to_mem, to_out = decision_thresholds()
    if weight >= to_mem: return Path.MEM.value
    if weight >= to_out: return Path.OUT.value
    return Path.TMP.value
