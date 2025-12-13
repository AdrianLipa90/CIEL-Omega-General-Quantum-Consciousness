"""Lightweight post-installation smoke test for the CIEL engine.

This script exercises the public API of the installable package without
relying on any local repository paths or the archival `ext/` directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ciel import CielEngine


def main() -> None:
    engine = CielEngine()
    result = engine.step("smoke test input")
    print("SMOKE TEST OK:", isinstance(result, dict), "keys:", sorted(result.keys()))


if __name__ == "__main__":
    main()
