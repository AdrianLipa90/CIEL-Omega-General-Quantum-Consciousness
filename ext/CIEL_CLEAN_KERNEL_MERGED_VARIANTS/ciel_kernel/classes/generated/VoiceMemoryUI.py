from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional
import numpy as np
import threading, queue, time

class VoiceMemoryUI:
    """Prosty rejestr głosowo-tekstowy – timeline pamięci."""
    entries: List[Dict[str, Any]] = field(default_factory=list)
    max_entries: int = 100

    def add_entry(self, text: str, mood: str='neutral'):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        self.entries.append({'time': timestamp, 'text': text, 'mood': mood})
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)

    def display(self, last_n: int=5):
        print('\n🧠 Voice Memory Timeline:')
        for e in self.entries[-last_n:]:
            color = {'neutral': '•', 'positive': '✦', 'negative': '⛒'}.get(e['mood'], '•')
            print(f" {color} [{e['time']}] {e['text']}")

    def export(self) -> List[Dict[str, Any]]:
        return list(self.entries)