"""Minimal stand-in for the vendor HDF5 store."""
from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Iterable, Sequence


class H5Store:
    """Persist vectors inside simple ``.h5`` JSON files.

    The implementation purposely avoids pulling heavy dependencies such as
    ``h5py`` while still exercising the filesystem interactions expected by the
    tests.  Each call to :meth:`append` creates a new ``.h5`` file containing a
    JSON payload with the stored vectors.
    """

    def __init__(self, root: Path | str = Path("data/waves")) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def append(self, symbol: str, intent: str, tensor: Sequence[float] | Iterable[float]) -> str:
        file_name = f"{symbol}_{intent}_{uuid.uuid4().hex}.h5"
        path = self.root / file_name
        data = {
            "symbol": symbol,
            "intent": intent,
            "tensor": list(tensor),
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)


__all__ = ["H5Store"]
