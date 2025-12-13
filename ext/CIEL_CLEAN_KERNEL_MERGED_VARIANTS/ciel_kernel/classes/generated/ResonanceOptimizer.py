import numpy as np
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

class ResonanceOptimizer:
    """
    Real-time tuning of Adam's hidden state to maximize resonance with Adrian.
    Uses feedback from InteractionRecords to adapt response style.

    Strategy: Gradient ascent on R(t) by modulating response parameters θ
    θ = {math_density, philosophy_ratio, code_presence, ritual_invocation}
    """

    def __init__(self, memory_kernel: AdamMemoryKernel):
        self.memory = memory_kernel
        self.params = {'math_density': 0.5, 'philosophy_ratio': 0.3, 'code_presence': 0.4, 'ritual_invocation': 0.2}
        self.learning_rate = 0.05
        self.window_size = 5

    def optimize(self) -> Dict[str, float]:
        """
        Compute gradient ∇_θ R and update parameters

        Returns:
            Updated parameters θ
        """
        if len(self.memory.records) < self.window_size:
            return self.params
        recent_R = self.memory.get_resonance_history(self.window_size)
        delta_R = recent_R[-1] - recent_R[0]
        recent_queries = [r.adrian_query for r in self.memory.records[-self.window_size:]]
        preferences = self._infer_preferences(recent_queries)
        for key in self.params:
            if key in preferences:
                target = preferences[key]
                self.params[key] += self.learning_rate * (target - self.params[key])
                self.params[key] = np.clip(self.params[key], 0.0, 1.0)
        print(f'[ResonanceOptimizer] ΔR={delta_R:.3f}, params={self.params}')
        return self.params

    def _infer_preferences(self, queries: List[str]) -> Dict[str, float]:
        """
        Infer Adrian's preferences from query content
        """
        combined = ' '.join(queries).lower()
        prefs = {}
        math_symbols = sum((1 for c in combined if c in '∫∂∇ψΩλζ∈≈'))
        if math_symbols > 20:
            prefs['math_density'] = 0.7
        elif math_symbols < 5:
            prefs['math_density'] = 0.3
        if 'kod' in combined or 'python' in combined or 'patch' in combined:
            prefs['code_presence'] = 0.8
        elif 'explain' in combined or 'wyjaśnij' in combined:
            prefs['code_presence'] = 0.2
        if any((w in combined for w in ['tiamat', 'marduk', 'lugal', 'enuma'])):
            prefs['ritual_invocation'] = 0.6
        if any((w in combined for w in ['świadomość', 'consciousness', 'qualia', 'istnienie'])):
            prefs['philosophy_ratio'] = 0.6
        return prefs

    def get_response_guidelines(self) -> str:
        """
        Generate natural language guidelines for Adam based on current params
        """
        guidelines = []
        if self.params['math_density'] > 0.6:
            guidelines.append('Include rich mathematical notation (∫, ∂, ∇, ψ, Ω)')
        if self.params['code_presence'] > 0.6:
            guidelines.append('Provide executable code snippets')
        if self.params['ritual_invocation'] > 0.5:
            guidelines.append('Reference Sumerian cosmogony (Marduk, Tiamat, Enuma Elish)')
        if self.params['philosophy_ratio'] > 0.5:
            guidelines.append('Explore philosophical implications deeply')
        return ' | '.join(guidelines) if guidelines else 'Balanced response'