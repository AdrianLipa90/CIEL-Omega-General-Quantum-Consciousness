"""Command-line interface for the CIEL Engine.

This module provides a lightweight entrypoint that can be invoked via
``python -m ciel``. It supports a REPL mode for interactive exploration and
an "once" mode for single-shot execution, emitting JSON for easy piping.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, List

from .engine import CielEngine


def setup_logging(level: str) -> None:
    """Configure basic logging for the CLI."""

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="CIEL/Ω unified engine")
    parser.add_argument("--mode", choices=["repl", "once"], default="repl")
    parser.add_argument("--text", type=str, default="", help="Input text for once mode.")
    parser.add_argument("--primary-model", type=str, default="mistral-7b-instruct")
    parser.add_argument("--aux-model", type=str, default="phi-3-mini-3.8b")
    parser.add_argument("--enable-llm", action="store_true", help="Attach HF language backends.")
    parser.add_argument(
        "--llm-backend",
        type=str,
        choices=["hf", "gguf"],
        default=None,
        help="Select LLM backend (default: env CIEL_LLM_BACKEND or hf).",
    )
    parser.add_argument(
        "--gguf-model-path",
        type=str,
        default=None,
        help="Path to a GGUF model file. Overrides env CIEL_GGUF_MODEL_PATH.",
    )
    parser.add_argument("--gguf-n-ctx", type=int, default=2048)
    parser.add_argument("--gguf-n-threads", type=int, default=4)
    parser.add_argument("--gguf-n-gpu-layers", type=int, default=0)
    parser.add_argument("--gguf-system-prompt", type=str, default="")
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser.parse_args(argv)


def _dump(obj: Dict[str, Any]) -> str:
    """Serialize results to JSON, handling numpy arrays if present."""

    def default(o: Any) -> Any:
        try:
            import numpy as np

            if isinstance(o, np.ndarray):
                return o.tolist()
        except Exception:
            pass
        return str(o)

    return json.dumps(obj, default=default, ensure_ascii=False, indent=2)


def run_repl(engine: CielEngine, enable_llm: bool) -> None:
    """Process lines from stdin, printing JSON results per line."""

    dialogue: List[Dict[str, str]] = []
    print("CIEL Engine REPL. Ctrl+D to exit.", file=sys.stderr)
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        result = _process_text(engine, line, enable_llm, dialogue)
        print(_dump(result))
        print()


def run_once(engine: CielEngine, text: str, enable_llm: bool) -> None:
    """Run the engine once with the provided text."""

    if not text.strip():
        print("No --text provided.", file=sys.stderr)
        sys.exit(1)
    result = _process_text(engine, text, enable_llm, [])
    print(_dump(result))


def _process_text(
    engine: CielEngine,
    text: str,
    enable_llm: bool,
    dialogue: List[Dict[str, str]],
) -> Dict[str, Any]:
    if not enable_llm:
        return engine.step(text)

    dialogue.append({"role": "user", "content": text})
    response = engine.interact(text, dialogue)
    reply = response.get("reply")
    if reply is not None:
        dialogue.append({"role": "assistant", "content": str(reply)})
    return response


def main(argv: list[str] | None = None) -> None:
    """Entry point used by ``python -m ciel``."""

    args = parse_args(argv)
    setup_logging(args.log_level)

    log = logging.getLogger("CIEL.CLI")
    log.info("Starting CielEngine in mode=%s", args.mode)

    engine = CielEngine()
    if args.enable_llm:
        try:
            from .llm_registry import build_default_bundle

            if args.gguf_model_path:
                os.environ["CIEL_GGUF_MODEL_PATH"] = args.gguf_model_path

            bundle = build_default_bundle(
                lite_model=args.primary_model,
                standard_model=args.primary_model,
                science_model=args.primary_model,
                analysis_model=args.aux_model,
                validator_model=args.aux_model,
                backend=args.llm_backend,
                gguf_n_ctx=args.gguf_n_ctx,
                gguf_n_threads=args.gguf_n_threads,
                gguf_n_gpu_layers=args.gguf_n_gpu_layers,
                gguf_system_prompt=args.gguf_system_prompt,
            )
            engine.language_backend = bundle.standard
            engine.aux_backend = bundle.composite_aux()
        except Exception as exc:
            log.warning("HF backends unavailable (%s); continuing without LLM.", exc)
    engine.boot()
    try:
        if args.mode == "repl":
            run_repl(engine, args.enable_llm)
        else:
            run_once(engine, args.text, args.enable_llm)
    finally:
        engine.shutdown()


if __name__ == "__main__":
    main()
