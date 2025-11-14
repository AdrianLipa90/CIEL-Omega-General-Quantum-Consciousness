"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from orchestrator import Orchestrator

def test_wtf_low_tokens():
    o=Orchestrator()
    res=o.process_input("?", user_subjective=0.0, self_subjective=0.0)
    assert res['status'] in ('WTF','TMP')  # depending on thresholds

def test_blocked_keyword():
    o=Orchestrator()
    res=o.process_input("WTFBLOCK content")
    assert res['status']=='BLOCKED'

def test_override_user_mem():
    o=Orchestrator()
    res=o.process_input("nauka design critical memo", user_save_override=True)
    assert res['status']=='MEM' and res.get('override', False)
