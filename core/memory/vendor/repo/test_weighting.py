"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from tmp.weighting import spectral_weight
from tmp.policy import Policy

def test_spectral_weight_basic():
    entry={'data':'nauka design memory kernel'}
    feats={'C':{'length':len(entry['data']),'tokens':len(entry['data'].split())},'M':{'symbol':'nauka','intent':'design'}}
    w=spectral_weight(entry,feats,0.3,0.1,Policy())
    assert w>=0.5
