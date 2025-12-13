from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import datetime, json, os, time, requests, sys, subprocess

def _demo():
    Bootstrap.ensure()
    ciel = CIELBatch3()
    f = np.random.rand(64, 64)
    Σ = ciel.measure_and_log(f, 'random_field_test')
    print(f'Σ (Soul Invariant) = {Σ:.4f}')
    print('Memory summary:', ciel.summary())