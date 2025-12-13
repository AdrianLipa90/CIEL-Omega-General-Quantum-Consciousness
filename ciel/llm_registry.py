from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import os
from pathlib import Path

from .language_backend import AuxiliaryBackend, LanguageBackend


class StubPrimary(LanguageBackend):
    def __init__(self, name: str, reason: str) -> None:
        self.name = name
        self._reason = reason

    def generate_reply(
        self,
        dialogue: List[Dict[str, str]],
        ciel_state: Dict[str, Any],
    ) -> str:
        last_user = ""
        for msg in reversed(dialogue):
            if msg.get("role") == "user":
                last_user = str(msg.get("content", ""))
                break
        return (
            f"[LLM unavailable: {self.name}] {self._reason}\n"
            f"User: {last_user}".strip()
        )


class StubAux(AuxiliaryBackend):
    def __init__(self, name: str, reason: str) -> None:
        self.name = name
        self._reason = reason

    def analyse_state(
        self,
        ciel_state: Dict[str, Any],
        candidate_reply: str,
    ) -> Dict[str, Any]:
        return {
            "backend": self.name,
            "available": False,
            "reason": self._reason,
            "candidate_reply": candidate_reply,
        }


@dataclass(slots=True)
class CompositeAuxBackend(AuxiliaryBackend):
    backends: List[AuxiliaryBackend] = field(default_factory=list)
    name: str = "composite-aux"

    def analyse_state(
        self,
        ciel_state: Dict[str, Any],
        candidate_reply: str,
    ) -> Dict[str, Any]:
        merged: Dict[str, Any] = {}
        for backend in self.backends:
            try:
                out = backend.analyse_state(ciel_state, candidate_reply)
            except Exception as exc:
                out = {"error": str(exc)}
            merged[backend.name] = out
        return merged


def _build_hf_backends() -> Tuple[type[LanguageBackend], type[AuxiliaryBackend]]:
    # Soft import: transformers might not be installed.
    from .hf_backends import AuxLLMBackend, PrimaryLLMBackend

    return PrimaryLLMBackend, AuxLLMBackend


def _build_gguf_backends() -> Tuple[type[LanguageBackend], type[AuxiliaryBackend]]:
    # Soft import: llama-cpp-python might not be installed.
    from .gguf_backends import GGUFAuxBackend, GGUFPrimaryBackend

    return GGUFPrimaryBackend, GGUFAuxBackend


def _candidate_gguf_dirs() -> List[Path]:
    seen: set[str] = set()
    dirs: List[Path] = []

    env_dir = os.getenv("CIEL_GGUF_MODELS_DIR")
    if env_dir:
        dirs.append(Path(env_dir))

    cwd = Path.cwd()
    dirs.append(cwd / "main" / "llm" / "models")
    dirs.append(cwd / "llm" / "models")

    # Repo-relative fallback (useful when running from the source tree)
    repo_root = Path(__file__).resolve().parent.parent
    dirs.append(repo_root / "main" / "llm" / "models")
    dirs.append(repo_root / "llm" / "models")

    out: List[Path] = []
    for d in dirs:
        if not d.is_dir():
            continue
        key = str(d.resolve())
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
    return out


def _resolve_profile_model_path(profile: str) -> Optional[str]:
    key = (profile or "").strip().lower()
    env_map = {
        "lite": "CIEL_GGUF_LITE_MODEL_PATH",
        "standard": "CIEL_GGUF_STANDARD_MODEL_PATH",
        "science": "CIEL_GGUF_SCIENCE_MODEL_PATH",
    }
    env_key = env_map.get(key)
    if env_key:
        val = os.getenv(env_key)
        if val:
            return val

    val = os.getenv("CIEL_GGUF_MODEL_PATH") or os.getenv("CIEL_GGUF_MODEL")
    if val:
        return val

    name_candidates = {
        "lite": ["lite.gguf", "basic.gguf", "ciel-lite.gguf", "ciel-basic.gguf"],
        "standard": ["standard.gguf", "medium.gguf", "ciel-standard.gguf", "ciel-medium.gguf"],
        "science": [
            "science.gguf",
            "special.gguf",
            "specialized.gguf",
            "ciel-science.gguf",
            "ciel-special.gguf",
        ],
    }

    candidates = name_candidates.get(key, [])
    for directory in _candidate_gguf_dirs():
        for fname in candidates:
            path = directory / fname
            if path.is_file():
                return str(path)

    # As a last resort, if the directory contains exactly one GGUF, use it.
    for directory in _candidate_gguf_dirs():
        ggufs = sorted(directory.glob("*.gguf"))
        if len(ggufs) == 1:
            return str(ggufs[0])

    return None


def _coerce_gguf_model_path(model_path: str) -> Optional[str]:
    if not model_path:
        return None

    path = Path(model_path)
    if path.is_file():
        return str(path)
    if path.is_dir():
        ggufs = sorted(path.glob("*.gguf"))
        if ggufs:
            return str(ggufs[0])
    return None


def build_primary_backend(
    *,
    model_name: str,
    device: Optional[str | int] = None,
    max_new_tokens: int = 256,
) -> LanguageBackend:
    try:
        PrimaryLLMBackend, _ = _build_hf_backends()
        return PrimaryLLMBackend(model_name=model_name, device=device, max_new_tokens=max_new_tokens)
    except Exception as exc:
        return StubPrimary(name=model_name, reason=f"{type(exc).__name__}: {exc}")


def build_aux_backend(
    *,
    model_name: str,
    device: Optional[str | int] = None,
    max_new_tokens: int = 128,
) -> AuxiliaryBackend:
    try:
        _, AuxLLMBackend = _build_hf_backends()
        return AuxLLMBackend(model_name=model_name, device=device, max_new_tokens=max_new_tokens)
    except Exception as exc:
        return StubAux(name=model_name, reason=f"{type(exc).__name__}: {exc}")


def build_gguf_primary_backend(
    *,
    model_path: str,
    n_ctx: int = 2048,
    n_threads: int = 4,
    n_gpu_layers: int = 0,
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    system_prompt: str = "",
) -> LanguageBackend:
    coerced = _coerce_gguf_model_path(model_path)
    if coerced is None:
        return StubPrimary(name="gguf", reason=f"GGUF model not found: {model_path}")
    model_path = coerced
    name = os.path.basename(model_path)
    try:
        from llama_cpp import Llama  # noqa: F401

        GGUFPrimaryBackend, _ = _build_gguf_backends()
        return GGUFPrimaryBackend(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            system_prompt=system_prompt,
        )
    except Exception as exc:
        return StubPrimary(name=name, reason=f"{type(exc).__name__}: {exc}")


def build_gguf_aux_backend(
    *,
    model_path: str,
    n_ctx: int = 2048,
    n_threads: int = 4,
    n_gpu_layers: int = 0,
    max_new_tokens: int = 128,
    temperature: float = 0.2,
    system_prompt: str = "",
) -> AuxiliaryBackend:
    coerced = _coerce_gguf_model_path(model_path)
    if coerced is None:
        return StubAux(name="gguf-aux", reason=f"GGUF model not found: {model_path}")
    model_path = coerced
    name = os.path.basename(model_path)
    try:
        from llama_cpp import Llama  # noqa: F401

        _, GGUFAuxBackend = _build_gguf_backends()
        return GGUFAuxBackend(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            system_prompt=system_prompt,
        )
    except Exception as exc:
        return StubAux(name=name, reason=f"{type(exc).__name__}: {exc}")


@dataclass(slots=True)
class LLMBackendBundle:
    lite: LanguageBackend
    standard: LanguageBackend
    science: LanguageBackend
    analysis: AuxiliaryBackend
    validator: AuxiliaryBackend

    def primary_for(self, profile: str) -> LanguageBackend:
        key = (profile or "").strip().lower()
        if key == "lite":
            return self.lite
        if key == "science":
            return self.science
        return self.standard

    def composite_aux(self) -> AuxiliaryBackend:
        analysis = self.analysis
        validator = self.validator

        class _NamedAux(AuxiliaryBackend):
            def __init__(self, name: str, backend: AuxiliaryBackend) -> None:
                self.name = name
                self._backend = backend

            def analyse_state(
                self,
                ciel_state: Dict[str, Any],
                candidate_reply: str,
            ) -> Dict[str, Any]:
                return self._backend.analyse_state(ciel_state, candidate_reply)

        backends: List[AuxiliaryBackend] = [
            _NamedAux(name=f"{analysis.name}:analysis", backend=analysis),
            _NamedAux(name=f"{validator.name}:validator", backend=validator),
        ]
        return CompositeAuxBackend(backends=backends)


def build_default_bundle(
    *,
    lite_model: str = "phi-3-mini-3.8b",
    standard_model: str = "mistral-7b-instruct",
    science_model: str = "qwen2.5-7b-instruct",
    analysis_model: str = "phi-3-mini-3.8b",
    validator_model: str = "mistral-7b-instruct",
    device: Optional[str | int] = None,
    backend: Optional[str] = None,
    gguf_n_ctx: int = 2048,
    gguf_n_threads: int = 4,
    gguf_n_gpu_layers: int = 0,
    gguf_system_prompt: str = "",
) -> LLMBackendBundle:
    resolved_backend = (backend or os.getenv("CIEL_LLM_BACKEND") or "hf").strip().lower()
    if resolved_backend in {"gguf", "llamacpp", "llama.cpp"}:
        lite_path = _resolve_profile_model_path("lite")
        standard_path = _resolve_profile_model_path("standard")
        science_path = _resolve_profile_model_path("science")
        aux_path = standard_path or lite_path or science_path

        return LLMBackendBundle(
            lite=(
                build_gguf_primary_backend(
                    model_path=lite_path,
                    n_ctx=gguf_n_ctx,
                    n_threads=gguf_n_threads,
                    n_gpu_layers=gguf_n_gpu_layers,
                    max_new_tokens=128,
                    temperature=0.7,
                    system_prompt=gguf_system_prompt,
                )
                if lite_path
                else StubPrimary(name="gguf-lite", reason="missing gguf model path")
            ),
            standard=(
                build_gguf_primary_backend(
                    model_path=standard_path,
                    n_ctx=gguf_n_ctx,
                    n_threads=gguf_n_threads,
                    n_gpu_layers=gguf_n_gpu_layers,
                    max_new_tokens=256,
                    temperature=0.7,
                    system_prompt=gguf_system_prompt,
                )
                if standard_path
                else StubPrimary(name="gguf-standard", reason="missing gguf model path")
            ),
            science=(
                build_gguf_primary_backend(
                    model_path=science_path,
                    n_ctx=gguf_n_ctx,
                    n_threads=gguf_n_threads,
                    n_gpu_layers=gguf_n_gpu_layers,
                    max_new_tokens=512,
                    temperature=0.5,
                    system_prompt=gguf_system_prompt,
                )
                if science_path
                else StubPrimary(name="gguf-science", reason="missing gguf model path")
            ),
            analysis=(
                build_gguf_aux_backend(
                    model_path=aux_path,
                    n_ctx=gguf_n_ctx,
                    n_threads=gguf_n_threads,
                    n_gpu_layers=gguf_n_gpu_layers,
                    max_new_tokens=128,
                    temperature=0.2,
                    system_prompt=gguf_system_prompt,
                )
                if aux_path
                else StubAux(name="gguf-aux", reason="missing gguf model path")
            ),
            validator=(
                build_gguf_aux_backend(
                    model_path=aux_path,
                    n_ctx=gguf_n_ctx,
                    n_threads=gguf_n_threads,
                    n_gpu_layers=gguf_n_gpu_layers,
                    max_new_tokens=128,
                    temperature=0.2,
                    system_prompt=gguf_system_prompt,
                )
                if aux_path
                else StubAux(name="gguf-aux", reason="missing gguf model path")
            ),
        )

    return LLMBackendBundle(
        lite=build_primary_backend(model_name=lite_model, device=device, max_new_tokens=128),
        standard=build_primary_backend(model_name=standard_model, device=device, max_new_tokens=256),
        science=build_primary_backend(model_name=science_model, device=device, max_new_tokens=512),
        analysis=build_aux_backend(model_name=analysis_model, device=device, max_new_tokens=128),
        validator=build_aux_backend(model_name=validator_model, device=device, max_new_tokens=128),
    )


__all__ = [
    "AuxiliaryBackend",
    "LanguageBackend",
    "CompositeAuxBackend",
    "LLMBackendBundle",
    "build_default_bundle",
    "build_primary_backend",
    "build_aux_backend",
    "build_gguf_primary_backend",
    "build_gguf_aux_backend",
]
