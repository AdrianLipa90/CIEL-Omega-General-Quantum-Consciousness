"""
LLM engine — offline-first, uses CielConfig attributes.
This version resolves model paths from the CielConfig object:
- llm_model_type (llamacpp | huggingface | cortex | mock)
- llm_model_name (folder name or filename)
It does NOT require a separate local_model_path attribute.
If the resolved model path does not exist, the engine falls back to a safe mock mode.
"""

import os
import json
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
import numpy as np

# Optional imports; we don't require them at import-time
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except Exception:
    TRANSFORMERS_AVAILABLE = False

# llama-cpp integration is imported lazily
LLAMA_CPP_AVAILABLE = False

@dataclass
class LLMConfig:
    """Internal config for LLMEngine (constructed from CielConfig)."""
    model_type: str = "mock"      # 'llamacpp', 'huggingface', 'cortex', or 'mock'
    model_name: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 512
    n_ctx: int = 2048
    n_threads: int = 4
    n_gpu_layers: int = 0
    # resolved path (determined at runtime)
    model_path: Optional[str] = None

class LLMEngine:
    """
    LLM Engine that resolves model path from a higher-level CielConfig object.
    It supports local backends:
      - llamacpp (.gguf) via llama-cpp-python (if installed)
      - huggingface (local files) via transformers (if installed)
      - cortex (.so) via ctypes
      - mock (fallback)
    """

    def __init__(self, config: Any, project_root: Optional[str] = None):
        """
        config: object (CielConfig) containing attributes such as:
            llm_model_type, llm_model_name, llm_temperature, llm_max_tokens
        project_root: optional path to project root; used to resolve models/
        """
        self.project_root = project_root or os.getcwd()
        # Build internal LLMConfig from provided config object (robust getattr)
        model_type = getattr(config, "llm_model_type", None) or getattr(config, "model_type", None) or "mock"
        model_name = getattr(config, "llm_model_name", None) or getattr(config, "model_name", None)
        temperature = getattr(config, "llm_temperature", None) or getattr(config, "temperature", 0.7)
        max_tokens = getattr(config, "llm_max_tokens", None) or getattr(config, "max_tokens", 512)
        n_threads = getattr(config, "llm_n_threads", None) or getattr(config, "n_threads", 4)
        n_gpu_layers = getattr(config, "llm_n_gpu_layers", None) or getattr(config, "n_gpu_layers", 0)

        self.config = LLMConfig(
            model_type=model_type.lower() if isinstance(model_type, str) else "mock",
            model_name=model_name,
            temperature=float(temperature),
            max_tokens=int(max_tokens),
            n_ctx=int(getattr(config, "llm_n_ctx", getattr(config, "n_ctx", 2048))),
            n_threads=int(n_threads),
            n_gpu_layers=int(n_gpu_layers)
        )

        # Resolve model path from project structure: models/...
        self._resolve_model_path()

        # Lazy attributes
        self.pipeline = None
        self.gguf_model = None
        self.ctypes_lib = None
        self.response_cache: Dict[str, Dict[str, Any]] = {}

        print(f"🧠 LLMEngine init: type={self.config.model_type}, name={self.config.model_name}, resolved_path={self.config.model_path}")

        # Initialize backend depending on resolved path/type
        if self.config.model_path and os.path.exists(self.config.model_path):
            if self.config.model_type == "llamacpp" or (str(self.config.model_path).lower().endswith(".gguf")):
                self._init_llamacpp()
            elif self.config.model_type == "huggingface":
                self._init_transformers()
            elif self.config.model_type == "cortex":
                self._init_cortex()
            else:
                print("⚠ Unrecognized model_type; falling back to mock.")
                self._init_mock()
        else:
            print("⚠ No valid local model found; using mock engine.")
            self._init_mock()

    def _resolve_model_path(self):
        """Resolve model_path based on project structure and config fields."""
        name = self.config.model_name
        p = None
        models_root = os.path.join(self.project_root, "models")
        # If explicit model_path was provided as a name that contains a path, use it
        if name and (os.path.isabs(name) or os.path.exists(os.path.join(self.project_root, name))):
            candidate = name if os.path.isabs(name) else os.path.join(self.project_root, name)
            if os.path.exists(candidate):
                p = candidate

        # Heuristics based on model_type
        if not p:
            if self.config.model_type == "llamacpp":
                # look for gguf file or folder
                folder = os.path.join(models_root, "llamacpp", name or "")
                if os.path.isdir(folder):
                    # prefer .gguf inside folder
                    for fname in os.listdir(folder):
                        if fname.lower().endswith(".gguf"):
                            p = os.path.join(folder, fname)
                            break
                    # or use folder directly if transformers-style
                    if not p:
                        p = folder
                else:
                    # maybe name is a file under models_root
                    candidate = os.path.join(models_root, "llamacpp", (name or ""))
                    if os.path.exists(candidate):
                        p = candidate
            elif self.config.model_type == "huggingface":
                folder = os.path.join(models_root, "huggingface.co", name or "")
                if os.path.isdir(folder):
                    p = folder
            elif self.config.model_type == "cortex":
                folder = os.path.join(models_root, "cortex.so", name or "")
                # try folder with .so inside or direct .so
                if os.path.isdir(folder):
                    for fname in os.listdir(folder):
                        if fname.lower().endswith(".so") or fname.lower().endswith(".dll"):
                            p = os.path.join(folder, fname)
                            break
                    if not p:
                        p = folder
                else:
                    candidate = os.path.join(models_root, "cortex.so", (name or ""))
                    if os.path.exists(candidate):
                        p = candidate

        # final fallback: scan models_root for anything that looks like a model if no name given
        if not p and os.path.isdir(models_root):
            # prefer llamacpp ggufs
            for top in ["llamacpp", "huggingface.co", "cortex.so"]:
                tdir = os.path.join(models_root, top)
                if os.path.isdir(tdir):
                    for entry in os.listdir(tdir):
                        candidate = os.path.join(tdir, entry)
                        if os.path.isdir(candidate):
                            p = candidate
                            break
                        if os.path.isfile(candidate) and candidate.lower().endswith((".gguf", ".so", ".dll")):
                            p = candidate
                            break
                if p:
                    break

        if p:
            self.config.model_path = os.path.abspath(p)
        else:
            self.config.model_path = None

    def _init_llamacpp(self):
        """Initialize llama-cpp backend if available."""
        global LLAMA_CPP_AVAILABLE
        try:
            from llama_cpp import Llama
            LLAMA_CPP_AVAILABLE = True
        except Exception as e:
            print(f"⚠ llama-cpp-python not available: {e}")
            LLAMA_CPP_AVAILABLE = False

        if not LLAMA_CPP_AVAILABLE:
            print("⚠ llama-cpp not installed; falling back to mock.")
            self._init_mock()
            return

        # if model_path is a folder, try to find .gguf inside
        model_path = self.config.model_path
        if os.path.isdir(model_path):
            gg = None
            for f in os.listdir(model_path):
                if f.lower().endswith(".gguf"):
                    gg = os.path.join(model_path, f)
                    break
            if gg:
                model_path = gg

        try:
            self.gguf_model = Llama(model_path=model_path, n_ctx=self.config.n_ctx, n_threads=self.config.n_threads)
            self.pipeline = None
            print(f"✓ GGUF model loaded: {model_path}")
        except Exception as e:
            print(f"⚠ Failed to load GGUF model: {e}")
            self._init_mock()

    def _init_transformers(self):
        """Initialize HuggingFace transformers backend (local files only)."""
        if not TRANSFORMERS_AVAILABLE:
            print("⚠ transformers not installed; falling back to mock.")
            self._init_mock()
            return
        model_path = self.config.model_path
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            self.model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)
            self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=-1)
            print(f"✓ HuggingFace model loaded from {model_path}")
        except Exception as e:
            print(f"⚠ Failed to load HuggingFace model: {e}")
            self._init_mock()

    def _init_cortex(self):
        """Initialize Cortex shared library via ctypes."""
        try:
            import ctypes
            lib = ctypes.CDLL(self.config.model_path)
            # expect generate_response signature
            if not hasattr(lib, "generate_response"):
                print("⚠ Cortex library has no generate_response entrypoint; falling back.")
                self._init_mock()
                return
            lib.generate_response.argtypes = [ctypes.c_char_p]
            lib.generate_response.restype = ctypes.c_char_p
            self.ctypes_lib = lib
            self.pipeline = lambda prompt, **kwargs: {"text": lib.generate_response(prompt.encode("utf-8")).decode("utf-8")}
            print(f"✓ Cortex library loaded: {self.config.model_path}")
        except Exception as e:
            print(f"⚠ Failed to load cortex library: {e}")
            self._init_mock()

    def _init_mock(self):
        """Fallback mock model for offline testing."""
        self.gguf_model = None
        self.ctypes_lib = None
        self.pipeline = None
        self.mock_responses = {
            "generate_intention": [
                "Promote coherence and life.",
                "Increase systemic harmony.",
                "Respect autonomy and minimize harm."
            ]
        }
        print("✓ Using mock LLM engine (no local model available)")

    def _generate_local(self, prompt: str) -> str:
        """Generate text using the available backend."""
        if self.gguf_model:
            try:
                out = self.gguf_model(prompt, max_tokens=self.config.max_tokens, temperature=self.config.temperature)
                # llama-cpp's callable may return dict or text depending on version
                if isinstance(out, dict):
                    return out.get("choices", [{}])[0].get("text", "") or out.get("text", "")
                return str(out)
            except Exception as e:
                print(f"⚠ GGUF generation error: {e}")
                return ""
        if self.pipeline:
            try:
                res = self.pipeline(prompt, max_length=self.config.max_tokens, temperature=self.config.temperature, do_sample=True, top_p=0.95, num_return_sequences=1)
                if isinstance(res, list) and res:
                    # HF pipeline
                    text = res[0].get("generated_text") or res[0].get("text")
                    return text if text else ""
                if isinstance(res, dict) and "text" in res:
                    return res["text"]
                return str(res)
            except Exception as e:
                print(f"⚠ Pipeline generation error: {e}")
                return ""
        # mock
        return np.random.choice(self.mock_responses.get("generate_intention", ["No model available."]))

    # Public helpers
    def generate_intention(self, context: str = "", emotional_state: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        prompt = (
            "Generate a consciousness intention. Context:\n" + (context or "")
        )
        text = self._generate_local(prompt)
        # simple processing
        return {"text": text}

    def __str__(self):
        return f"LLMEngine(type={self.config.model_type}, path={self.config.model_path})"
