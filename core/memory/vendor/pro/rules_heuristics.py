import json, re
from pathlib import Path
from typing import Dict, Any
class RuleHeuristicsEngine:
    def __init__(self, cfg_dir: Path):
        self.cfg_dir = Path(cfg_dir)
        self.immutable = json.loads((self.cfg_dir / "rules_immutable.json").read_text(encoding="utf-8"))
        self.user = json.loads((self.cfg_dir / "heuristics_user.json").read_text(encoding="utf-8"))
        self.selfcfg = json.loads((self.cfg_dir / "heuristics_self.json").read_text(encoding="utf-8"))
    def ethical_gate(self, text: str) -> bool:
        for pat in self.immutable.get("forbidden_patterns", []):
            if re.search(pat, text, flags=re.IGNORECASE): return False
        return True
    def weight(self, D_dict: Dict[str, Any]) -> Dict[str, float]:
        sense = str(D_dict.get("D_S", "")).strip(); meta = D_dict.get("D_M", {}) or {}; associations = D_dict.get("D_A", []) or []
        logic = 0.6 if len(sense) >= 32 else 0.4
        semantic = 0.6 if len(sense.split()) >= 5 else 0.4
        context = 0.55 if D_dict.get("D_C") else 0.3
        emotion = 0.5
        u = self.user
        if meta.get("trusted_source"): logic += u["boosts"].get("trusted_source", 0)
        if meta.get("novelty_hint"): semantic += u["boosts"].get("novelty_hint", 0)
        if meta.get("contradiction_flag"): logic += u["penalties"].get("contradiction_flag", -0.25)
        if meta.get("ethics_warning"): semantic += u["penalties"].get("ethics_warning", -0.50)
        s = self.selfcfg
        if len(sense) >= 120: logic += s["boosts"].get("long_form", 0.10)
        if associations: context += s["boosts"].get("associations_present", 0.05)
        if len(sense) < 8: semantic += s["penalties"].get("too_short", -0.15)
        def _cl(x): return max(0.0, min(1.0, x))
        return {"W_L": _cl(logic), "W_S": _cl(semantic), "W_K": _cl(context), "W_E": _cl(emotion)}
