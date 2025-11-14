"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from .tmp_kernel import TMPKernel, DataVector
from .types import MemoriseD
from .durable_tsm_sqlite import TSMWriterSQL
from .durable_wpm_hdf5 import WPMWriterHDF5
from .audit_log import AuditLog
import uuid, datetime as dt

class UnifiedMemoryOrchestrator:
    def __init__(self, cfg_dir: Path = Path("configs"),
                 tsm_db: Path = Path("CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db"),
                 wpm_h5: Path = Path("CIEL_MEMORY_SYSTEM/WPM/wave_snapshots/wave_archive.h5"),
                 audit_path: Path = Path("CIEL_MEMORY_SYSTEM/AUDIT/ledger.jsonl")):
        cfg_dir.mkdir(parents=True, exist_ok=True); tsm_db.parent.mkdir(parents=True, exist_ok=True); wpm_h5.parent.mkdir(parents=True, exist_ok=True)
        self.tsm = TSMWriterSQL(tsm_db)
        self.wpm = WPMWriterHDF5(wpm_h5)
        self.tmp = TMPKernel(cfg_dir)
        self.audit = AuditLog(audit_path)
        self._tmp_reports: List[Dict[str, Any]] = []
        self._verification_queue: List[Dict[str, Any]] = []
        self.allow_system_force_save = True
        self.allow_user_force_save = True

    def capture(self, context: str, sense: Any, associations=None, timestamp=None, meta=None) -> DataVector:
        return DataVector(context=context, sense=sense, associations=associations, timestamp=timestamp, meta=meta)

    def run_tmp(self, D: DataVector) -> Dict[str, Any]:
        out = self.tmp.process(D)
        verdict = out["OUT"]["verdict"]
        level = "INFO" if verdict == "PASS" else ("IMPORTANT" if verdict == "HOLD" else "CRITICAL")
        rep = {"report_id": str(uuid.uuid4()), "created_at": dt.datetime.utcnow().isoformat(), "level": level,
               "payload": {"D_id": D.id, "OUT": out}, "requires_user_verification": level != "INFO", "verified_by_user": False}
        self._tmp_reports.append(rep)
        if rep["requires_user_verification"]: self._verification_queue.append(rep)
        self.audit.append("TMP_OUT", {"D_id": D.id, "verdict": verdict})
        return out

    def _make_memorised(self, D: DataVector, a1: Dict[str, Any], a2: Dict[str, Any], rationale: str, source: str = "TMP") -> MemoriseD:
        return MemoriseD(memorise_id=str(uuid.uuid4()), created_at=dt.datetime.utcnow().isoformat(),
                         D_id=D.id, D_context=D.D_C, D_sense=D.D_S, D_associations=D.D_A, D_timestamp=D.D_T, D_meta=D.D_M,
                         D_type=a1.get("D_TYPE","unknown"), D_attr=a1.get("D_ATTR",{}), weights=a2.get("weights",{}),
                         rationale=rationale, source=source)

    def _save_dual(self, mem: MemoriseD, wave_arrays: Optional[Dict[str, "np.ndarray"]] = None, wave_attrs: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        tsm_ref = self.tsm.save(mem)
        if wave_arrays or wave_attrs: wpm_ref = self.wpm.save_with_wave(mem, wave_arrays=wave_arrays, attrs=wave_attrs)
        else: wpm_ref = self.wpm.save(mem)
        self.tsm.attach_wpm_ref(mem.memorise_id, wpm_ref)
        self.audit.append("DURABLE_WRITE", {"memorise_id": mem.memorise_id, "tsm_ref": tsm_ref, "wpm_ref": wpm_ref})
        return {"tsm_ref": tsm_ref, "wpm_ref": wpm_ref, "memorise_id": mem.memorise_id}

    def promote_if_bifurcated(self, D: DataVector, tmp_out: Dict[str, Any], wave_arrays: Optional[Dict[str, "np.ndarray"]] = None, wave_attrs: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, str]]:
        a2, a1 = tmp_out["OUT"], tmp_out.get("A1", {})
        if a2.get("verdict") == "PASS" and a2.get("bifurcation") == 1:
            mem = self._make_memorised(D, a1, a2, rationale="B=1 collapse from TMP.")
            return self._save_dual(mem, wave_arrays=wave_arrays, wave_attrs=wave_attrs)
        return None

    def user_force_save(self, D: DataVector, tmp_out: Dict[str, Any], reason: str, wave_arrays: Optional[Dict[str, "np.ndarray"]] = None, wave_attrs: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, str]]:
        if not self.allow_user_force_save: return None
        a2, a1 = tmp_out["OUT"], tmp_out.get("A1", {})
        mem = self._make_memorised(D, a1, a2, rationale=f"User override: {reason}", source="USER_OVERRIDE")
        return self._save_dual(mem, wave_arrays=wave_arrays, wave_attrs=wave_attrs)

    def daily_maintenance(self) -> Dict[str, int]:
        kept, purged = 0, 0; new_reports = []
        for r in self._tmp_reports:
            if r["level"] == "INFO": purged += 1
            else: kept += 1; new_reports.append(r)
        self._tmp_reports = new_reports
        self._verification_queue = [r for r in self._tmp_reports if r["requires_user_verification"] and not r["verified_by_user"]]
        self.audit.append("DAILY_MAINTENANCE", {"kept": kept, "purged": purged, "pending": len(self._verification_queue)})
        return {"kept": kept, "purged": purged, "pending_verifications": len(self._verification_queue)}
