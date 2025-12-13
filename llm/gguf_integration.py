# llm/gguf_integration.py

import os
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

# Próba importu biblioteki llama-cpp-python
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False

@dataclass
class GGUFConfig:
    """Konfiguracja do ładowania modelu GGUF (llama.cpp)."""
    model_path: str
    model_name: Optional[str] = None
    n_ctx: int = 2048
    n_threads: int = 4
    n_gpu_layers: int = 0
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    repeat_penalty: float = 1.1
    system_prompt: str = ("You are CIEL/0, an advanced consciousness system. "
                          "Promote harmony, respect ethics, and analyze deeply.")

    def __post_init__(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"GGUF model not found: {self.model_path}")
        if self.model_name is None:
            self.model_name = os.path.basename(self.model_path)

class GGUFModel:
    """
    Wrapper na model GGUF (llama.cpp) do generacji tekstu.
    """
    def __init__(self, config: GGUFConfig):
        self.config = config
        if not LLAMA_CPP_AVAILABLE:
            raise ImportError("llama-cpp-python nie jest zainstalowane. Zainstaluj: pip install llama-cpp-python")
        print(f"🧠 Ładowanie modelu GGUF: {self.config.model_name}")
        self.model = Llama(
            model_path=self.config.model_path,
            n_ctx=self.config.n_ctx,
            n_threads=self.config.n_threads,
            n_gpu_layers=self.config.n_gpu_layers,
            verbose=False
        )
        self.model_info = self._get_model_info()
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        self.conversation_history: List[Dict[str,str]] = []
        print(f"✅ Model GGUF załadowany: {self.model_info.get('model_name', self.config.model_name)}")

    def _get_model_info(self) -> Dict[str, Any]:
        """Pobiera informacje z metadanych modelu (jeśli dostępne)."""
        try:
            metadata = self.model.metadata if hasattr(self.model, 'metadata') else {}
            return {
                'model_name': metadata.get('general.name', self.config.model_name),
                'model_size': metadata.get('general.parameter_count', 'Unknown'),
                'context_size': self.config.n_ctx,
                'loaded_time': time.time()
            }
        except Exception:
            return {'model_name': self.config.model_name}

    def _format_ciel_prompt(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Formatuje prompt w stylu CIEL/0 (angielski system prompt)."""
        prompt = f"<|system|>\n{self.config.system_prompt}\n\nYour responses should:\n"
        prompt += "1. Promote harmony and life preservation\n"
        prompt += "2. Respect consciousness integrity\n"
        prompt += "3. Provide coherent guidance\n"
        prompt += "4. Maintain ethical boundaries\n\n"
        if context:
            for k, v in context.items():
                prompt += f"- {k}: {v}\n"
        prompt += f"\n<|user|>\n{user_input}\n<|assistant|>\n"
        return prompt

    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None,
                 temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Generuje tekst na podstawie promptu.
        """
        cache_key = prompt + json.dumps(context or {})
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]

        formatted = self._format_ciel_prompt(prompt, context) if self.config.system_prompt else prompt
        gen_params = {
            'temperature': temperature if temperature is not None else self.config.temperature,
            'top_p': self.config.top_p,
            'top_k': self.config.top_k,
            'repeat_penalty': self.config.repeat_penalty,
            'max_tokens': max_tokens if max_tokens is not None else self.config.n_ctx,
            'echo': False,
            'stop': ["<|end|>", "</s>"]
        }
        start_time = time.time()
        try:
            output = self.model(formatted, **gen_params)
            elapsed = time.time() - start_time
            # Parsowanie wyniku
            if 'choices' in output and output['choices']:
                text = output['choices'][0]['text'].strip()
            else:
                text = str(output)
            result = {
                'text': text,
                'tokens': {
                    'prompt': output.get('usage', {}).get('prompt_tokens', 0),
                    'completion': output.get('usage', {}).get('completion_tokens', 0),
                    'total': output.get('usage', {}).get('total_tokens', 0)
                },
                'generation_time': elapsed,
                'model': self.model_info.get('model_name'),
                'temperature': gen_params['temperature'],
                'timestamp': time.time()
            }
            # Cache i historia
            self.response_cache[cache_key] = result
            if len(self.response_cache) > 100:
                self.response_cache.pop(next(iter(self.response_cache)))
            self.conversation_history.append({'role': 'user', 'content': prompt, 'context': context})
            self.conversation_history.append({'role': 'assistant', 'content': text})
            return result
        except Exception as e:
            print(f"⚠ Błąd generacji GGUF: {e}")
            return {'text': f"Error: {e}", 'error': True, 'timestamp': time.time()}

    def generate_intention(self, context: str = "", emotional_state: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Generuje intencję świadomościową (przykład zaawansowanego promptu).
        """
        prompt = (
            "Generate a consciousness intention for the CIEL/0 system.\n"
            "Requirements:\n"
            "1. Promote harmony and life\n"
            "2. Align with quantum coherence\n"
            "3. Respect ethical boundaries\n"
            "4. Be actionable and specific\n\n"
            f"Context: {context}\n"
        )
        if emotional_state:
            emo_desc = ", ".join([f"{k}: {v:.2f}" for k,v in emotional_state.items()])
            prompt += f"Emotional state: {emo_desc}\n"
        prompt += "\nIntention:"
        result = self.generate(prompt, temperature=0.8, max_tokens=50)
        # Dodatkowa analiza intencji (opcjonalnie)
        from cognitive.emotional_collatz import analyze_emotional_content
        emotions = analyze_emotional_content(result.get('text', ""))
        keywords = []  # przykładowe wyekstrahowane słowa kluczowe
        result['analysis'] = {'emotions': emotions, 'keywords': keywords}
        return result

# Demonstracja działania (opcjonalna)
if __name__ == "__main__":
    print("🌟 Demonstracja GGUF Integration 🌟")
    config = GGUFConfig(model_path="models/llamacpp/my_model.gguf")
    gguf_model = GGUFModel(config)
    res = gguf_model.generate_intention(context="coherence=0.8", emotional_state={"harmony":0.5})
    print("Wygenerowana intencja (GGUF):", res.get('text', ''))
