from __future__ import annotations

from typing import Any, Dict, List, Optional
import json

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

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


class PrimaryLLMBackend(LanguageBackend):
    def __init__(
        self,
        model_name: str,
        device: Optional[str | int] = None,
        max_new_tokens: int = 256,
    ) -> None:
        self.name = model_name
        self.device = device
        self.max_new_tokens = max_new_tokens
        self._pipe = None

    def _lazy_init(self) -> None:
        if self._pipe is None:
            tokenizer = AutoTokenizer.from_pretrained(self.name)
            model = AutoModelForCausalLM.from_pretrained(self.name)
            self._pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=self.device,
            )

    def _format_dialogue(self, dialogue: List[Dict[str, str]]) -> str:
        lines: List[str] = []
        for message in dialogue:
            role = message.get("role", "user")
            content = message.get("content", "")
            lines.append(f"{role.capitalize()}: {content}")
        return "\n".join(lines)

    def _summarize_state(self, ciel_state: Dict[str, Any]) -> str:
        summary = {
            "intention_vector": ciel_state.get("intention_vector"),
            "simulation": _reduce_simulation(ciel_state.get("simulation")),
            "cognition": ciel_state.get("cognition"),
            "affect": ciel_state.get("affect"),
        }
        return json.dumps(summary, ensure_ascii=False, default=_json_default)

    def generate_reply(
        self,
        dialogue: List[Dict[str, str]],
        ciel_state: Dict[str, Any],
    ) -> str:
        self._lazy_init()
        prompt_parts = [self._format_dialogue(dialogue), "State:", self._summarize_state(ciel_state)]
        prompt = "\n".join(part for part in prompt_parts if part)

        outputs = self._pipe(prompt, max_new_tokens=self.max_new_tokens)
        if not outputs:
            return ""
        generated = outputs[0].get("generated_text", "")
        if generated.startswith(prompt):
            generated = generated[len(prompt) :]
        return generated.strip()


class AuxLLMBackend(AuxiliaryBackend):
    def __init__(
        self,
        model_name: str,
        device: Optional[str | int] = None,
        max_new_tokens: int = 128,
    ) -> None:
        self.name = model_name
        self.device = device
        self.max_new_tokens = max_new_tokens
        self._pipe = None

    def _lazy_init(self) -> None:
        if self._pipe is None:
            tokenizer = AutoTokenizer.from_pretrained(self.name)
            model = AutoModelForCausalLM.from_pretrained(self.name)
            self._pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=self.device,
            )

    def _build_prompt(self, ciel_state: Dict[str, Any], candidate_reply: str) -> str:
        summary = {
            "intention_vector": ciel_state.get("intention_vector"),
            "simulation": _reduce_simulation(ciel_state.get("simulation")),
            "cognition": ciel_state.get("cognition"),
            "affect": ciel_state.get("affect"),
        }
        state_json = json.dumps(summary, ensure_ascii=False, default=_json_default)
        return (
            "Evaluate the following reply for coherence and helpfulness given the state. "
            "Provide JSON with keys coherence, helpfulness, keywords, emotion.\n"
            f"State: {state_json}\n"
            f"Reply: {candidate_reply}\n"
        )

    def _parse_output(self, text: str) -> Dict[str, Any]:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass
        return {"raw": text.strip()}

    def analyse_state(
        self,
        ciel_state: Dict[str, Any],
        candidate_reply: str,
    ) -> Dict[str, Any]:
        self._lazy_init()
        prompt = self._build_prompt(ciel_state, candidate_reply)
        outputs = self._pipe(prompt, max_new_tokens=self.max_new_tokens)
        if not outputs:
            return {"raw": ""}
        generated = outputs[0].get("generated_text", "")
        if generated.startswith(prompt):
            generated = generated[len(prompt) :]
        return self._parse_output(generated)


__all__ = ["PrimaryLLMBackend", "AuxLLMBackend"]
