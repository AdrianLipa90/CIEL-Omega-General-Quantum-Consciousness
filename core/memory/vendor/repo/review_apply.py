"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import json, sys
from pathlib import Path
from orchestrator import Orchestrator

# Apply verification decisions from a JSON file with entries:
# {"decisions":[{"data":"...", "symbol":"...", "intent":"...", "approve":true}]}
def main():
    if len(sys.argv)<2:
        print("Usage: python scripts/review_apply.py <decisions.json>")
        return
    dec_path = Path(sys.argv[1])
    if not dec_path.exists():
        print("Decisions file not found")
        return
    o = Orchestrator()
    dec = json.loads(dec_path.read_text(encoding='utf-8'))
    applied = 0
    for d in dec.get('decisions', []):
        data = d.get('data')
        if not data: 
            continue
        if d.get('approve', False):
            res = o.process_input(data, user_save_override=True)
        else:
            res = {"status":"REJECTED"}
        applied += 1
        print(res)
    print(f"Applied: {applied} decisions")

if __name__ == "__main__":
    main()
