from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Tuple

from .language_backend import AuxiliaryBackend, LanguageBackend


def _json_default(obj: Any) -> Any:
    try:
        import numpy as np

        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
    except Exception:
        pass

    if isinstance(obj, (set, tuple)):
        return list(obj)

    return str(obj)


_LLAMA_CACHE: Dict[Tuple[str, int, int, int], Any] = {}


def _coerce_role(role: str) -> str:
    key = (role or "").strip().lower()
    if key in {"system", "user", "assistant"}:
        return key
    return "user"


def _format_dialogue(dialogue: List[Dict[str, str]]) -> str:
    lines: List[str] = []
    for message in dialogue:
        role = _coerce_role(str(message.get("role", "user"))).capitalize()
        content = str(message.get("content", ""))
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _reduce_simulation(simulation: Any) -> Any:
    if not isinstance(simulation, dict):
        return simulation

    reduced: Dict[str, Any] = {}

    if simulation.get("lambda0") is not None:
        reduced["lambda0"] = simulation.get("lambda0")
    if simulation.get("raw") is not None:
        reduced["raw"] = simulation.get("raw")

    field = simulation.get("field")
    if field is not None:
        try:
            rows = len(field)
            cols = len(field[0]) if rows else 0
            reduced["field_shape"] = [rows, cols]
        except Exception:
            reduced["field_shape"] = None

    tensor = simulation.get("resonance_tensor")
    if tensor is not None:
        try:
            reduced["resonance_tensor_head"] = [row[:3] for row in tensor[:3]]
        except Exception:
            reduced["resonance_tensor_head"] = tensor

    return reduced


def _summarize_state(ciel_state: Dict[str, Any]) -> str:
    summary = {
        "intention_vector": ciel_state.get("intention_vector"),
        "simulation": _reduce_simulation(ciel_state.get("simulation")),
        "cognition": ciel_state.get("cognition"),
        "affect": ciel_state.get("affect"),
    }
    return json.dumps(summary, ensure_ascii=False, default=_json_default)


def _extract_text(output: Any) -> str:
    if isinstance(output, dict):
        choices = output.get("choices") or []
        if choices:
            choice0 = choices[0] or {}
            message = choice0.get("message") or {}
            if isinstance(message, dict) and message.get("content") is not None:
                return str(message.get("content"))
            if choice0.get("text") is not None:
                return str(choice0.get("text"))
        if output.get("text") is not None:
            return str(output.get("text"))
    return str(output)


def _parse_json_object(text: str) -> Dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            return {"raw": text.strip()}
    return {"raw": text.strip()}


class GGUFPrimaryBackend(LanguageBackend):
    def __init__(
        self,
        *,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        system_prompt: str = "",
    ) -> None:
        self.model_path = model_path
        self.n_ctx = int(n_ctx)
        self.n_threads = int(n_threads)
        self.n_gpu_layers = int(n_gpu_layers)
        self.max_new_tokens = int(max_new_tokens)
        self.temperature = float(temperature)
        self.system_prompt = system_prompt
        self.name = os.path.basename(model_path) if model_path else "gguf"
        self._llama: Any | None = None

    def _lazy_init(self) -> None:
        if self._llama is not None:
            return
        key = (self.model_path, self.n_ctx, self.n_threads, self.n_gpu_layers)
        cached = _LLAMA_CACHE.get(key)
        if cached is not None:
            self._llama = cached
            return

        from llama_cpp import Llama

        llama = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=False,
        )
        _LLAMA_CACHE[key] = llama
        self._llama = llama

    def generate_reply(self, dialogue: List[Dict[str, str]], ciel_state: Dict[str, Any]) -> str:
        self._lazy_init()
        state_json = _summarize_state(ciel_state)

        system = self.system_prompt.strip()
        if system:
            system = system + "\n\n"
        system += f"State: {state_json}"

        llama = self._llama
        if llama is None:
            return ""

        if hasattr(llama, "create_chat_completion"):
            messages: List[Dict[str, str]] = [{"role": "system", "content": system}]
            for msg in dialogue:
                messages.append(
                    {
                        "role": _coerce_role(str(msg.get("role", "user"))),
                        "content": str(msg.get("content", "")),
                    }
                )
            out = llama.create_chat_completion(
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_new_tokens,
            )
            return _extract_text(out).strip()

        prompt_parts = [system, _format_dialogue(dialogue), "Assistant:"]
        prompt = "\n".join(part for part in prompt_parts if part)
        out = llama(
            prompt,
            temperature=self.temperature,
            max_tokens=self.max_new_tokens,
            stop=["User:", "System:", "Assistant:"],
        )
        return _extract_text(out).strip()


class GGUFAuxBackend(AuxiliaryBackend):
    def __init__(
        self,
        *,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        max_new_tokens: int = 128,
        temperature: float = 0.2,
        system_prompt: str = "",
    ) -> None:
        self.model_path = model_path
        self.n_ctx = int(n_ctx)
        self.n_threads = int(n_threads)
        self.n_gpu_layers = int(n_gpu_layers)
        self.max_new_tokens = int(max_new_tokens)
        self.temperature = float(temperature)
        self.system_prompt = system_prompt
        self.name = os.path.basename(model_path) if model_path else "gguf-aux"
        self._llama: Any | None = None

    def _lazy_init(self) -> None:
        if self._llama is not None:
            return
        key = (self.model_path, self.n_ctx, self.n_threads, self.n_gpu_layers)
        cached = _LLAMA_CACHE.get(key)
        if cached is not None:
            self._llama = cached
            return

        from llama_cpp import Llama

        llama = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=False,
        )
        _LLAMA_CACHE[key] = llama
        self._llama = llama

    def analyse_state(self, ciel_state: Dict[str, Any], candidate_reply: str) -> Dict[str, Any]:
        self._lazy_init()
        state_json = _summarize_state(ciel_state)

        prompt_parts = [
            self.system_prompt.strip(),
            "Evaluate the following reply for coherence and helpfulness given the state.",
            "Return JSON with keys coherence, helpfulness, keywords, emotion.",
            f"State: {state_json}",
            f"Reply: {candidate_reply}",
        ]
        prompt = "\n".join(part for part in prompt_parts if part)

        llama = self._llama
        if llama is None:
            return {"raw": ""}

        out = llama(
            prompt,
            temperature=self.temperature,
            max_tokens=self.max_new_tokens,
            stop=["User:", "System:", "Assistant:"],
        )
        text = _extract_text(out)
        return _parse_json_object(text)


__all__ = ["GGUFPrimaryBackend", "GGUFAuxBackend"]
