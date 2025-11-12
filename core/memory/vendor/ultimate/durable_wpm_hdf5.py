import json
from pathlib import Path
from typing import Any, Dict, Optional

from .types import MemoriseD

try:
    import h5py
except Exception:
    h5py = None

class WPMWriterHDF5:
    def __init__(self, h5_path: Path):
        if h5py is None: raise RuntimeError("h5py is required for WPMWriterHDF5. Install with: pip install h5py")
        self.h5_path = Path(h5_path); self.h5_path.parent.mkdir(parents=True, exist_ok=True)
        with h5py.File(self.h5_path, "a") as h5:
            if "memories" not in h5: h5.create_group("memories")

    def save(self, record: MemoriseD) -> str:
        with h5py.File(self.h5_path, "a") as h5:
            grp = h5["memories"].create_group(record.memorise_id) if record.memorise_id not in h5["memories"] else h5["memories"][record.memorise_id]
            def _s(n, v): 
                if n in grp: del grp[n]; grp.create_dataset(n, data=str(v))
            def _j(n, o):
                if n in grp: del grp[n]; grp.create_dataset(n, data=json.dumps(o, ensure_ascii=False))
            _s("created_at", record.created_at); _s("D_id", record.D_id); _s("D_context", record.D_context); _s("D_sense", str(record.D_sense))
            _j("D_associations", record.D_associations); _s("D_timestamp", record.D_timestamp); _j("D_meta", record.D_meta)
            _s("D_type", record.D_type); _j("D_attr", record.D_attr); _j("weights", record.weights); _s("rationale", record.rationale); _s("source", record.source)
        return f"WPM:{record.memorise_id}"

    def save_with_wave(self, record: MemoriseD, wave_arrays: Optional[Dict[str, "np.ndarray"]] = None, attrs: Optional[Dict[str, Any]] = None) -> str:
        if h5py is None: raise RuntimeError("h5py is required for WPMWriterHDF5.")
        import numpy as np
        with h5py.File(self.h5_path, "a") as h5:
            root = h5["memories"]
            grp = root.create_group(record.memorise_id) if record.memorise_id not in root else root[record.memorise_id]
            def _s(n, v): 
                if n in grp: del grp[n]; grp.create_dataset(n, data=str(v))
            def _j(n, o):
                if n in grp: del grp[n]; grp.create_dataset(n, data=json.dumps(o, ensure_ascii=False))
            _s("created_at", record.created_at); _s("D_id", record.D_id); _s("D_context", record.D_context); _s("D_sense", str(record.D_sense))
            _j("D_associations", record.D_associations); _s("D_timestamp", record.D_timestamp); _j("D_meta", record.D_meta)
            _s("D_type", record.D_type); _j("D_attr", record.D_attr); _j("weights", record.weights); _s("rationale", record.rationale); _s("source", record.source)
            if wave_arrays:
                waves = grp.create_group("waves") if "waves" not in grp else grp["waves"]
                for name, arr in wave_arrays.items():
                    if name in waves: del waves[name]
                    waves.create_dataset(name, data=arr)
            if attrs:
                for k, v in attrs.items():
                    try: grp.attrs[k] = v
                    except Exception: grp.attrs[k] = str(v)
        return f"WPM:{record.memorise_id}"
