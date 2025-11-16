"""Command-line interface for the CIEL Engine.

This module provides a lightweight entrypoint that can be invoked via
``python -m ciel``. It supports a REPL mode for interactive exploration and
an "once" mode for single-shot execution, emitting JSON for easy piping.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Any, Dict

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


def run_repl(engine: CielEngine) -> None:
    """Process lines from stdin, printing JSON results per line."""

    print("CIEL Engine REPL. Ctrl+D to exit.", file=sys.stderr)
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        result = engine.step(line)
        print(_dump(result))
        print()


def run_once(engine: CielEngine, text: str) -> None:
    """Run the engine once with the provided text."""

    if not text.strip():
        print("No --text provided.", file=sys.stderr)
        sys.exit(1)
    result = engine.step(text)
    print(_dump(result))


def main(argv: list[str] | None = None) -> None:
    """Entry point used by ``python -m ciel``."""

    args = parse_args(argv)
    setup_logging(args.log_level)

    log = logging.getLogger("CIEL.CLI")
    log.info("Starting CielEngine in mode=%s", args.mode)

    engine = CielEngine()
    engine.boot()
    try:
        if args.mode == "repl":
            run_repl(engine)
        else:
            run_once(engine, args.text)
    finally:
        engine.shutdown()


if __name__ == "__main__":
    main()
