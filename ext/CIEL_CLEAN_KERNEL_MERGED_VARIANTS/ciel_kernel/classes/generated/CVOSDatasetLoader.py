from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

class CVOSDatasetLoader:
    """Loader datasetów CVOS (sigile, glyphy, Z-serie)."""
    base_path: str = '.'

    def load_json(self, filename: str) -> List[Dict[str, Any]]:
        """Ładuje sygle CVOS (JSON)."""
        path = os.path.join(self.base_path, filename)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        if 'sigils' in data:
            return data['sigils']
        elif isinstance(data, list):
            return data
        else:
            return [data]

    def load_txt(self, filename: str) -> List[Dict[str, Any]]:
        """Ładuje pliki Z-serii TXT (np. cvos.glyphs.Z5)."""
        path = os.path.join(self.base_path, filename)
        entries = []
        current = {}
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ':' in line:
                    k, v = line.split(':', 1)
                    k, v = (k.strip(), v.strip())
                    if k in current:
                        entries.append(current)
                        current = {}
                    current[k] = v
            if current:
                entries.append(current)
        return entries