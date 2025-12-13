from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import datetime, json, os, time, requests, sys, subprocess

class Bootstrap:
    """Light bootstrapper verifying dependencies and setup."""
    required = {'numpy': 'numpy', 'requests': 'requests'}

    @staticmethod
    def ensure():
        print('🔍 Checking core dependencies...')
        for lib, pkg in Bootstrap.required.items():
            try:
                __import__(lib)
                print(f'✓ Found {lib}')
            except ImportError:
                print(f'⚠ Missing {lib}, installing...')
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
        print('Environment verified ✓')