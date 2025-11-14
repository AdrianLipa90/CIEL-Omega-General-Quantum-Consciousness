
"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Compatibility orchestrator for the open-source repo profile.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping

from persistent import H5Store, Journal, PersistentMemory, rotate_tmp_reports
from tmp import (
    Heuristics,
    Policy,
    analyze_input,
    capture,
    compute_weight,
    decide_branch,
    daily_report,
    prefilter,
)
from utils import color_tag, encode_tensor_scalar


@dataclass
class _TmpEntry:
    data: str
    features: Mapping[str, Mapping[str, Any]]
    capture: Any
    weight: float
    g_score: float
    m_score: float
    status: str
    created_at: datetime = field(default_factory=datetime.utcnow)


class Orchestrator:
    """Sane reimplementation of the vendor orchestrator stub."""

    def __init__(self) -> None:
        self.tmp_memory: List[_TmpEntry] = []
        self.mem = PersistentMemory()
        self.h5 = H5Store()
        self.journal = Journal()
        self.policy = Policy()
        self._heuristics = Heuristics()

    # ------------------------------------------------------------------ flow
    def process_input(
        self,
        data: str,
        user_subjective: float = 0.0,
        self_subjective: float = 0.0,
        user_save_override: bool = False,
        system_save_override: bool = False,
    ) -> Dict[str, Any]:
        raw = prefilter(data)
        if raw is None:
            self.journal.log("drop", {"reason": "empty"})
            return {"status": "dropped"}

        capture_envelope = capture(raw)
        features = analyze_input(raw)
        blocked, reason = self._heuristics.check_blockers(raw)
        if blocked:
            self.journal.log("blocked", {"reason": reason, "data": raw})
            return {"status": "BLOCKED", "reason": reason}

        tokens = int(features.get("C", {}).get("tokens", 0))
        if tokens < 2 and not (user_save_override or system_save_override):
            self.journal.log("wtf", {"data": raw, "tokens": tokens})
            return {"status": "WTF", "question": "Please clarify context."}

        weight, g_score, m_score, ctx = compute_weight(
            {"data": raw}, features, user_subjective, self_subjective, self.policy
        )
        entry = _TmpEntry(
            data=raw,
            features=features,
            capture=capture_envelope,
            weight=weight,
            g_score=g_score,
            m_score=m_score,
            status="TMP",
        )

        should_override = user_save_override or system_save_override
        if should_override:
            saved = self._persist_to_memory(entry, tokens, override=True)
            self.journal.log(
                "mem_store_override",
                {"symbol": ctx["symbol"], "intent": ctx["intent"], "weight": weight, "override": True},
            )
            entry.status = "MEM"
            self.tmp_memory.append(entry)
            return {"status": "MEM", "override": True, "weight": weight, "saved": saved}

        branch = decide_branch(weight, self.policy.spectral_conf().get("decision"))
        if branch == "mem":
            saved = self._persist_to_memory(entry, tokens, override=False)
            entry.status = "MEM"
            self.tmp_memory.append(entry)
            self.journal.log("mem_store", {"symbol": ctx["symbol"], "intent": ctx["intent"], "weight": weight})
            return {"status": "MEM", "saved": saved}
        if branch == "out":
            entry.status = "OUT"
            self.tmp_memory.append(entry)
            self.journal.log("tmp_hold", {"weight": weight})
            return {"status": "OUT", "weight": weight}

        entry.status = "TMP"
        self.tmp_memory.append(entry)
        return {"status": "TMP", "weight": weight}

    # -------------------------------------------------------------- persistence
    def _persist_to_memory(self, entry: _TmpEntry, tokens: int, override: bool) -> Dict[str, Any]:
        symbol = entry.features.get("M", {}).get("symbol", "default")
        intent = entry.features.get("M", {}).get("intent", "general")
        colour = color_tag(entry.m_score)
        table = {
            "Lp": len(self.mem.clusters.get(symbol, {}).get(intent, [])) + 1,
            "Ref": uuid.uuid4().hex,
            "Date": datetime.utcnow().isoformat(),
            "Context": entry.features.get("T", {}).get("type", ""),
            "Links": [],
            "G": float(entry.g_score),
            "M": float(entry.m_score),
            "ColorOS": colour,
            "Override": override,
        }
        tensor = encode_tensor_scalar(entry.weight, entry.g_score, entry.m_score, tokens)
        saved = self.mem.store(symbol, intent, tensor, metadata={"data": entry.data}, table=table)
        self.h5.append(symbol, intent, tensor)
        return saved

    # ------------------------------------------------------------------ reports
    def daily(self) -> Dict[str, Any]:
        report = daily_report({"status": e.status} for e in self.tmp_memory)
        report_path = Path("data/tmp_reports") / f"tmp_report_{report['date']}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        migrated = 0
        for entry in list(self.tmp_memory):
            if entry.status == "TMP" and entry.weight >= 1.2:
                tokens = int(entry.features.get("C", {}).get("tokens", 0))
                self._persist_to_memory(entry, tokens, override=False)
                entry.status = "MEM"
                migrated += 1

        rotate_tmp_reports()
        self.journal.log("daily_close", {"migrated": migrated, "report": report})
        return {"report": report, "migrated": migrated}


__all__ = ["Orchestrator"]
