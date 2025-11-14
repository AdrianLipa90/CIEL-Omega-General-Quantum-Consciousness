"""Test-friendly implementation of the ``UnifiedMemoryOrchestrator``."""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DataVector:
    """Container capturing the pieces of information that flow through TMP."""

    context: str
    sense: Any
    associations: Optional[Any] = None
    timestamp: Optional[datetime] = None
    meta: Optional[Dict[str, Any]] = None
    id: str = field(init=False, repr=False)

    def __post_init__(self) -> None:  # type: ignore[override]
        object.__setattr__(self, "id", uuid.uuid4().hex)
        object.__setattr__(self, "D_C", self.context)
        object.__setattr__(self, "D_S", self.sense)
        object.__setattr__(self, "D_A", self.associations)
        object.__setattr__(self, "D_T", self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else None)
        object.__setattr__(self, "D_M", self.meta or {})


class UnifiedMemoryOrchestrator:
    """Very small orchestrator used for the kata exercises.

    The class tracks a ledger stored in ``CIEL_MEMORY_SYSTEM`` and exposes just
    enough functionality for the tests: capturing data vectors, running them
    through a toy TMP pipeline and persisting the result when bifurcation or a
    manual override requests it.
    """

    def __init__(self) -> None:
        base = Path("CIEL_MEMORY_SYSTEM")
        self._ledger_path = base / "TSM" / "ledger" / "memory_ledger.db"
        self._wave_dir = base / "WPM" / "wave_snapshots"
        self._ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._wave_dir.mkdir(parents=True, exist_ok=True)
        if not self._ledger_path.exists():
            self._ledger_path.write_text("", encoding="utf-8")
        self._tmp_reports: List[Dict[str, Any]] = []
        self._verification_queue: List[Dict[str, Any]] = []
        self.allow_user_force_save = True

    # ------------------------------------------------------------------ TMP
    def capture(
        self,
        context: str,
        sense: Any,
        associations: Any | None = None,
        timestamp: datetime | None = None,
        meta: Dict[str, Any] | None = None,
    ) -> DataVector:
        return DataVector(context=context, sense=sense, associations=associations, timestamp=timestamp, meta=meta)

    def run_tmp(self, D: DataVector) -> Dict[str, Any]:
        text = str(D.sense)
        tokens = len(text.split())
        novelty = 1.0 if (D.meta or {}).get("novelty_hint") else 0.6
        verdict = "PASS" if tokens >= 5 else ("HOLD" if tokens >= 2 else "REJECT")
        bifurcation = 1 if verdict == "PASS" and novelty >= 0.8 else 0
        out = {
            "OUT": {
                "verdict": verdict,
                "bifurcation": bifurcation,
                "weights": {"novelty": novelty, "length": tokens},
            },
            "A1": {
                "D_TYPE": "text",
                "D_ATTR": {"tokens": tokens, "novelty_hint": bool((D.meta or {}).get("novelty_hint"))},
            },
        }
        report = {
            "report_id": uuid.uuid4().hex,
            "created_at": datetime.utcnow().isoformat(),
            "payload": {"D_id": D.id, "OUT": out},
            "requires_user_verification": verdict != "PASS",
            "verified_by_user": False,
        }
        self._tmp_reports.append(report)
        if report["requires_user_verification"]:
            self._verification_queue.append(report)
        return out

    # ----------------------------------------------------------------- save
    def _make_entry(self, D: DataVector, tmp_out: Dict[str, Any], rationale: str, source: str) -> Dict[str, Any]:
        entry = {
            "memorise_id": uuid.uuid4().hex,
            "captured_at": datetime.utcnow().isoformat(),
            "context": D.context,
            "sense": D.sense,
            "meta": D.meta or {},
            "rationale": rationale,
            "source": source,
            "tmp_out": tmp_out.get("OUT", {}),
        }
        return entry

    def _persist_entry(self, entry: Dict[str, Any]) -> Dict[str, str]:
        with self._ledger_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        wave_file = self._wave_dir / f"{entry['memorise_id']}.json"
        wave_file.write_text(json.dumps(entry["tmp_out"], ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "tsm_ref": str(self._ledger_path),
            "wpm_ref": str(wave_file),
            "memorise_id": entry["memorise_id"],
        }

    def promote_if_bifurcated(
        self,
        D: DataVector,
        tmp_out: Dict[str, Any],
        wave_arrays: Optional[Dict[str, Any]] = None,
        wave_attrs: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, str]]:
        if tmp_out.get("OUT", {}).get("bifurcation") == 1:
            entry = self._make_entry(D, tmp_out, "Auto promotion after bifurcation", "TMP")
            return self._persist_entry(entry)
        return None

    def user_force_save(
        self,
        D: DataVector,
        tmp_out: Dict[str, Any],
        reason: str,
        wave_arrays: Optional[Dict[str, Any]] = None,
        wave_attrs: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, str]]:
        if not self.allow_user_force_save:
            return None
        entry = self._make_entry(D, tmp_out, f"User override: {reason}", "USER_OVERRIDE")
        return self._persist_entry(entry)

    # ----------------------------------------------------------- maintenance
    def daily_maintenance(self) -> Dict[str, int]:
        kept = [r for r in self._tmp_reports if r["requires_user_verification"]]
        purged = len(self._tmp_reports) - len(kept)
        self._tmp_reports = kept
        self._verification_queue = [r for r in kept if not r["verified_by_user"]]
        return {
            "kept": len(kept),
            "purged": purged,
            "pending_verifications": len(self._verification_queue),
        }


__all__ = ["UnifiedMemoryOrchestrator", "DataVector"]
