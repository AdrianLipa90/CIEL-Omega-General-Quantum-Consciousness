from typing import Any, Dict, List, Optional
from .si_utils import validate_timestamp
from .spectral_multiplier import gamma_from_categories, evaluate_spectral_categories
from .rules_heuristics import RuleHeuristicsEngine
from pathlib import Path
import uuid, datetime as dt

class DataVector:
    def __init__(self, context: str, sense: Any, associations: Optional[List[Any]] = None,
                 timestamp: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
        self.id = str(uuid.uuid4())
        self.D_C = context; self.D_S = sense; self.D_A = associations or []
        self.D_T = timestamp or dt.datetime.utcnow().isoformat(); self.D_M = meta or {}

class TMPKernel:
    def __init__(self, cfg_dir: Path):
        self.rh = RuleHeuristicsEngine(cfg_dir)
        self.immutable_rules = {"require_context": True, "require_sense": True, "ethical_gate": True}

    def first_analysis(self, D: DataVector) -> Dict[str, Any]:
        if not D.D_C or not D.D_S:
            return {"verdict": "FAIL", "response": "WTF? Missing context or sense.", "bifurcation": 0}
        ok_ts, norm_ts = validate_timestamp(D.D_T)
        if not ok_ts:
            return {"verdict": "FAIL", "response": "WTF? Invalid timestamp (non-ISO8601).", "bifurcation": 0}
        D.D_T = norm_ts or D.D_T
        if isinstance(D.D_S, str) and len(D.D_S.strip()) >= 4:
            return {"verdict": "PASS", "D_TYPE": "text", "D_ATTR": {"length": len(D.D_S)}, "bifurcation": 0}
        return {"verdict": "HOLD", "response": "WTF? Provide more context.", "bifurcation": 0}

    def second_analysis(self, D: DataVector, D_TYPE: str, D_ATTR: Dict[str, Any]) -> Dict[str, Any]:
        text = str(D.D_S)
        if self.immutable_rules["ethical_gate"] and not self.rh.ethical_gate(text):
            return {"verdict": "REJECT", "reason": "Ethical gate failed.", "bifurcation": 0}
        base = self.rh.weight({"D_C": D.D_C, "D_S": D.D_S, "D_A": D.D_A, "D_T": D.D_T, "D_M": D.D_M, "D_TYPE": D_TYPE, "D_ATTR": D_ATTR})
        cat = evaluate_spectral_categories({"D_C": D.D_C, "D_S": D.D_S, "D_A": D.D_A, "D_T": D.D_T, "D_M": D.D_M, "D_TYPE": D_TYPE, "D_ATTR": D_ATTR})
        gamma = gamma_from_categories(cat)
        Wp = {k: (v * gamma if isinstance(v, float) else v) for k, v in base.items()}
        W_total = (Wp["W_L"] + Wp["W_S"] + Wp["W_K"] + Wp["W_E"]) / 4.0
        if W_total < 0.40: return {"verdict": "REJECT", "reason": "Too weak.", "weights": Wp, "gamma": gamma, "categories": cat, "bifurcation": 0}
        if W_total < 0.70: return {"verdict": "HOLD", "reason": "Needs clarification.", "weights": Wp, "gamma": gamma, "categories": cat, "bifurcation": 0}
        return {"verdict": "PASS", "weights": Wp, "gamma": gamma, "categories": cat, "bifurcation": 1}

    def process(self, D: DataVector) -> Dict[str, Any]:
        a1 = self.first_analysis(D)
        if a1["verdict"] != "PASS": return {"OUT": a1, "report": "A1 pending user context or failed."}
        a2 = self.second_analysis(D, a1["D_TYPE"], a1["D_ATTR"])
        return {"OUT": a2, "report": {"REJECT": "Blocked by RULE/HEUR.", "HOLD": "Awaiting user input.", "PASS": "Logical pass."}[a2["verdict"]], "A1": a1}
