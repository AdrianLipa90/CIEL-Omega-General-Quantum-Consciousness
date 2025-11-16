"""CLI entrypoint for running the :class:`CielEngine`.

Usage:
    python -m ciel
"""

from __future__ import annotations

import json
from typing import Any

from .engine import CielEngine


def main(argv: list[str] | None = None) -> int:
    """Run the engine once and print the structured output as JSON."""

    _ = argv  # placeholder for future argument parsing
    engine = CielEngine()
    result: dict[str, Any] = engine.process()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
