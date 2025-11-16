"""CLI entrypoint for running the :class:`CielEngine`."""

from __future__ import annotations

import json
from typing import Any

from .engine import CielEngine


def main(argv: list[str] | None = None) -> int:
    """Run the engine once and print the structured output as JSON."""

    _ = argv  # placeholder for future argument parsing
    engine = CielEngine()
    engine.boot()
    result: dict[str, Any] = engine.step("Hello, CIEL")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    engine.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
