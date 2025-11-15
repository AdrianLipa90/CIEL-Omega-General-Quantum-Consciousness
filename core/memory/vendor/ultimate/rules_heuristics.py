"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

import json, re
from pathlib import Path
from typing import Dict, Any

class RuleHeuristicsEngine:
    def __init__(self, cfg_dir: Path):
        self.cfg_dir = Path(cfg_dir)
        self.immutable = self._load("rules_immutable.json", {
            "require_context": True, "require_sense": True, "ethical_gate": True,
            "forbidden_patterns": ["illegal","harm","exploit"]
        })
        self.user = self._load("heuristics_user.json", {
            "weights":{"logic":0.35,"semantic":0.25,"context":0.20,"emotion":0.20},
            "boosts":{"novelty_hint":0.15,"trusted_source":0.10},
            "penalties":{"contradiction_flag":-0.25,"ethics_warning":-0.50}
        })
        self.selfcfg = self._load("heuristics_self.json", {
            "weights":{"logic":0.30,"semantic":0.25,"context":0.25,"emotion":0.20},
            "boosts":{"long_form":0.10,"associations_present":0.05},
            "penalties":{"too_short":-0.15}
        })

    def _load(self, name: str, default_obj: Dict[str, Any]) -> Dict[str, Any]:
        p = self.cfg_dir / name
        if p.exists():
            try: return json.loads(p.read_text(encoding="utf-8"))
            except Exception: pass
        return json.loads(json.dumps(default_obj))

    def ethical_gate(self, text: str) -> bool:
        if not self.immutable.get("ethical_gate", True): return True
        for pat in self.immutable.get("forbidden_patterns", []):
            if re.search(pat, text or "", flags=re.IGNORECASE): return False
        return True

    def weight(self, D_dict: Dict[str, Any]) -> Dict[str, float]:
        sense = str(D_dict.get("D_S","")).strip()
        meta = D_dict.get("D_M",{}) or {}
        associations = D_dict.get("D_A",[]) or []

        logic = 0.6 if len(sense) >= 32 else 0.4
        semantic = 0.6 if len(sense.split()) >= 5 else 0.4
        context = 0.55 if D_dict.get("D_C") else 0.30
        emotion = 0.50

        u = self.user
        if meta.get("trusted_source"): logic += u["boosts"].get("trusted_source", 0.10)
        if meta.get("novelty_hint"): semantic += u["boosts"].get("novelty_hint", 0.15)
        if meta.get("contradiction_flag"): logic += u["penalties"].get("contradiction_flag", -0.25)
        if meta.get("ethics_warning"): semantic += u["penalties"].get("ethics_warning", -0.50)

        s = self.selfcfg
        if len(sense) >= 120: logic += s["boosts"].get("long_form", 0.10)
        if associations: context += s["boosts"].get("associations_present", 0.05)
        if len(sense) < 8: semantic += s["penalties"].get("too_short", -0.15)

        def _cl(x: float) -> float:
            return max(0.0, min(1.0, x))

        return {"W_L": _cl(logic), "W_S": _cl(semantic), "W_K": _cl(context), "W_E": _cl(emotion)}
