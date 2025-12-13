from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import math, re, hashlib, numpy as np

def demonstracja_emocjonalnego_collatza():
    print('🎭 EMOCJONALNY COLLATZ – DEMO')
    engine = EmotionalCollatzEngine()
    testowe_intencje = ['Kocham życie i wszystko co ze sobą niesie – pełen entuzjazmu i radości', 'Obawiam się przyszłości, ale pragnę znaleźć w sobie siłę i odwagę', 'Jestem zły na niesprawiedliwość świata, ale chcę to zmienić przez działanie', 'Czuję głęboki spokój i jedność z wszechświatem – wszystko jest idealne', 'Smutek miesza się z nadzieją w poszukiwaniu sensu istnienia']
    for i, intencja in enumerate(testowe_intencje, 1):
        print(f'\n🧠 TEST {i}: {intencja[:72]}…')
        out = engine.execute_emotional_program(intencja, input_data=42)
        final = out['final_result']
        metrics = out['metrics']
        land = out['emotional_landscape']
        print(f'   📊 final_result ≈ {final.real:+.4e} + {final.imag:+.4e}j')
        print(f"   📈 emotional_coherence={metrics['emotional_coherence']:.4f} | heart_mind_coherence={metrics['heart_mind_coherence']:.4f}")
        print(f"   🎭 dominant={land['dominant_emotion']} | patterns={', '.join(land['emotional_resonance_pattern'])}")