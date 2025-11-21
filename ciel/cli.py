"""Command-line entry points for the CIEL engine.

The CLI exposes lightweight helpers so installed environments can
instantiate and exercise the 12D kernel without relying on repository
paths or manual script wiring.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from ciel import CielEngine


def _run_engine(text: str) -> Dict[str, Any]:
    engine = CielEngine()
    return engine.step(text)


def run_engine() -> None:
    """Execute a single engine step from the command line."""

    parser = argparse.ArgumentParser(description="Run the CIEL engine over a prompt")
    parser.add_argument(
        "text",
        nargs="?",
        default="hello from CIEL",
        help="Input text to feed into the intention/emotion/memory pipeline",
    )
    args = parser.parse_args()

    result = _run_engine(args.text)
    print(json.dumps(result, indent=2, sort_keys=True))


def smoke_test() -> None:
    """Run the lightweight smoke test shipped with the package installation."""

    result = _run_engine("post-installation smoke test")
    ok = result.get("status") == "ok"
    keys = sorted(result.keys())
    print(f"SMOKE TEST {'OK' if ok else 'FAILED'}: keys={keys}")


if __name__ == "__main__":
    run_engine()
