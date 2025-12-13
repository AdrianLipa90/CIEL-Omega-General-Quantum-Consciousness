#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CIEL/0 – Unified Reality Kernel
Główny punkt wejścia systemu
"""
import time
import json
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import threading
from queue import Queue
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main() -> None:
    from ciel.__main__ import main as ciel_main

    ciel_main(sys.argv[1:])

if __name__ == "__main__":
    main()