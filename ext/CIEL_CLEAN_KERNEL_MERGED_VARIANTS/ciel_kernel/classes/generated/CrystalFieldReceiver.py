from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional
import numpy as np
import threading, queue, time

class CrystalFieldReceiver:
    """Symulowany odbiornik sygnału pola krystalicznego."""
    geometry: str = 'hexagonal-core'
    status: str = field(default='idle', init=False)
    intent_field: Optional[np.ndarray] = field(default=None, init=False)

    def receive(self, signal: np.ndarray) -> Dict[str, Any]:
        """
        Odbiera i dekoduje sygnał wejściowy.
        Zwraca jego podpis (signature) oraz współczynnik koherencji.
        """
        from math import sin, pi
        self.status = 'resonating'
        self.intent_field = signal
        encoded = np.array([sin(i * pi / 8) for i in range(16)]) * np.mean(signal)
        coherence = float(np.mean(np.abs(encoded)))
        signature = np.mean(encoded) + 1j * np.std(encoded)
        return {'status': self.status, 'geometry': self.geometry, 'coherence': round(coherence, 5), 'signature': signature}