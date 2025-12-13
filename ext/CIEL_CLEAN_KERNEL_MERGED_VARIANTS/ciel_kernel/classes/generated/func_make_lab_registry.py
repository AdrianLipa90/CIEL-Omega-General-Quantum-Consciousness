from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Tuple, Optional
import numpy as np, time, math, random

def make_lab_registry() -> ExpRegistry:
    reg = ExpRegistry()
    reg.add('c01', exp_c01)
    reg.add('c02', exp_c02)
    reg.add('a2ebdead', exp_a2ebdead)
    reg.add('47fdb331', exp_47fdb331)
    reg.add('72b221d9', exp_72b221d9)
    reg.add('rcde_calibrated', exp_rcde_calibrated)
    reg.add('ResCxParKer_lite', exp_rescxparker_lite)
    reg.add('VYCH_BOOT_RITUAL', exp_vych_boot_ritual)
    reg.add('dissociation', exp_dissociation)
    reg.add('noweparadoxy', exp_noweparadoxy)
    return reg