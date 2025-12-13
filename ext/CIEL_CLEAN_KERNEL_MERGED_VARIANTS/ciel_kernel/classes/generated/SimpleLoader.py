from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import datetime, json, os, time, requests, sys, subprocess

class SimpleLoader:
    """Minimal loader for local/remote binary or numeric data."""
    dtype_map = {8: np.uint8, 16: np.int16, 32: np.int32, -32: np.float32}

    @staticmethod
    def fetch(url_or_path: str) -> bytes:
        if url_or_path.startswith('http'):
            return requests.get(url_or_path, stream=True).content
        with open(url_or_path, 'rb') as f:
            return f.read()

    @staticmethod
    def parse_header(data: bytes) -> Dict[str, Any]:
        header, pos = (b'', 0)
        while b'END' not in header and pos < len(data):
            header += data[pos:pos + 2880]
            pos += 2880
        hdr = {}
        for i in range(0, len(header), 80):
            card = header[i:i + 80].decode('ascii', errors='ignore').strip()
            if card.startswith('END'):
                break
            if '=' in card:
                k, rest = card.split('=', 1)
                k = k.strip()
                v = rest.split('/')[0].strip().strip("'")
                try:
                    v = float(v) if '.' in v else int(v)
                except:
                    pass
                hdr[k] = v
        return hdr