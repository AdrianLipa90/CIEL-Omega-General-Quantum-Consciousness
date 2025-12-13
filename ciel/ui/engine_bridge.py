from __future__ import annotations

import os
import threading
import time
from typing import Any, Dict, List, Optional


class EngineBridge:
    def __init__(self, settings: Dict[str, Any]):
        self._lock = threading.Lock()
        self.settings: Dict[str, Any] = dict(settings)
        self.dialogue: List[Dict[str, str]] = []
        self.last_latency_ms: Optional[float] = None
        self.last_lambda0: Optional[float] = None

        self.engine = None
        self.llm_bundle = None

        try:
            from ..engine import CielEngine

            self.engine = CielEngine()
            try:
                self.engine.boot()
            except Exception:
                pass
        except Exception:
            self.engine = None

        self.apply_settings(self.settings)

    def is_available(self) -> bool:
        return self.engine is not None

    def apply_settings(self, settings: Dict[str, Any]) -> None:
        self.settings = dict(settings)

        if self.engine is None:
            return

        backend = (self.settings.get("backend") or "hf").strip().lower()
        os.environ["CIEL_LLM_BACKEND"] = backend

        try:
            from ..llm_registry import build_default_bundle

            if backend == "gguf":
                gguf_cfg = self.settings.get("gguf") or {}

                models_dir = str(gguf_cfg.get("models_dir") or "").strip()
                lite_path = str(gguf_cfg.get("lite_model_path") or "").strip()
                standard_path = str(gguf_cfg.get("standard_model_path") or "").strip()
                science_path = str(gguf_cfg.get("science_model_path") or "").strip()

                if models_dir:
                    os.environ["CIEL_GGUF_MODELS_DIR"] = models_dir
                else:
                    os.environ.pop("CIEL_GGUF_MODELS_DIR", None)

                if lite_path:
                    os.environ["CIEL_GGUF_LITE_MODEL_PATH"] = lite_path
                else:
                    os.environ.pop("CIEL_GGUF_LITE_MODEL_PATH", None)

                if standard_path:
                    os.environ["CIEL_GGUF_STANDARD_MODEL_PATH"] = standard_path
                else:
                    os.environ.pop("CIEL_GGUF_STANDARD_MODEL_PATH", None)

                if science_path:
                    os.environ["CIEL_GGUF_SCIENCE_MODEL_PATH"] = science_path
                else:
                    os.environ.pop("CIEL_GGUF_SCIENCE_MODEL_PATH", None)

                if gguf_cfg.get("system_prompt") is not None:
                    os.environ["CIEL_GGUF_SYSTEM_PROMPT"] = str(gguf_cfg.get("system_prompt") or "")

                self.llm_bundle = build_default_bundle(
                    backend="gguf",
                    gguf_n_ctx=int(gguf_cfg.get("n_ctx") or 2048),
                    gguf_n_threads=int(gguf_cfg.get("n_threads") or 4),
                    gguf_n_gpu_layers=int(gguf_cfg.get("n_gpu_layers") or 0),
                    gguf_system_prompt=str(gguf_cfg.get("system_prompt") or ""),
                )
            else:
                hf_cfg = self.settings.get("hf") or {}
                self.llm_bundle = build_default_bundle(
                    backend="hf",
                    lite_model=str(hf_cfg.get("lite_model") or "phi-3-mini-3.8b"),
                    standard_model=str(hf_cfg.get("standard_model") or "mistral-7b-instruct"),
                    science_model=str(hf_cfg.get("science_model") or "qwen2.5-7b-instruct"),
                    analysis_model=str(hf_cfg.get("analysis_model") or "phi-3-mini-3.8b"),
                    validator_model=str(hf_cfg.get("validator_model") or "mistral-7b-instruct"),
                    device=hf_cfg.get("device"),
                )
        except Exception:
            self.llm_bundle = None

    def reset_dialogue(self) -> None:
        self.dialogue = []

    def _select_profile(self, profile: str) -> str:
        key = (profile or "").strip().lower()
        if key in {"lite", "standard", "science"}:
            return key
        if key in {"ultra", "max", "maximum"}:
            return "science"
        return "standard"

    def interact(
        self,
        *,
        user_text: str,
        mode: str,
        profile: str,
        memory: Optional[str] = None,
    ) -> Dict[str, Any]:
        if self.engine is None:
            return {"status": "no_engine"}

        selected_profile = self._select_profile(profile)
        mode_key = (mode or "dialogue").strip().lower() or "dialogue"
        memory_key = (memory or "").strip().lower()
        context = f"{mode_key}:{memory_key}" if memory_key else mode_key
        history_limit = int(((self.settings.get("chat") or {}).get("history_limit") or 40))

        with self._lock:
            if self.llm_bundle is not None:
                self.engine.language_backend = self.llm_bundle.primary_for(selected_profile)
                self.engine.aux_backend = self.llm_bundle.composite_aux()

            if history_limit > 0 and len(self.dialogue) > history_limit:
                self.dialogue = self.dialogue[-history_limit:]

            self.dialogue.append({"role": "user", "content": user_text})

            t0 = time.perf_counter()
            result = self.engine.interact(user_text, self.dialogue, context=context)
            self.last_latency_ms = (time.perf_counter() - t0) * 1000.0

            reply = result.get("reply")
            if reply is not None:
                self.dialogue.append({"role": "assistant", "content": str(reply)})

            if history_limit > 0 and len(self.dialogue) > history_limit:
                self.dialogue = self.dialogue[-history_limit:]

            try:
                self.last_lambda0 = float(
                    (((result.get("ciel_state") or {}).get("simulation") or {}).get("lambda0"))
                )
            except Exception:
                self.last_lambda0 = None

            return result

    def step_status(self) -> Optional[Dict[str, Any]]:
        if self.engine is None:
            return None
        with self._lock:
            try:
                result = self.engine.step("status")
                try:
                    self.last_lambda0 = float(((result.get("simulation") or {}).get("lambda0")))
                except Exception:
                    self.last_lambda0 = None
                return result
            except Exception:
                return None

    def shutdown(self) -> None:
        with self._lock:
            try:
                if self.engine is not None:
                    self.engine.shutdown()
            except Exception:
                pass


__all__ = ["EngineBridge"]
