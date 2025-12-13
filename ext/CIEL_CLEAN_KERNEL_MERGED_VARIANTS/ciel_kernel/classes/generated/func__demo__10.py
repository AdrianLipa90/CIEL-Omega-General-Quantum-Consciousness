from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, numpy as np, os

def _demo():
    loader = CVOSDatasetLoader(base_path='/mnt/data/CIEL_extracted/CIEL')
    try:
        sigils = loader.load_json('CVOS_GliphSigils_MariaKamecka.json')
        print(f'Loaded {len(sigils)} sigils from CVOS.')
    except Exception as e:
        print('Could not load CVOS dataset:', e)
        sigils = []
    n1 = GlyphNode(id='GLIF_GEN.01C', name='Glyph of the First Symphony', code='intent.sound[α₁] >> field.init(resonance)', field_key='CVOS::GENESIS_01', operator_signature='INT::LIPA.001')
    n2 = GlyphNode(id='GLIF_HEL.04C', name='Glyph of the Double Helix', code='intent.duality[Ω₂] >> chain.twist(A∩T/G∩C)', field_key='CVOS::HELIX', operator_signature='INT::LIPA.001')
    interp = GlyphNodeInterpreter()
    interp.register(n1)
    interp.register(n2)
    interp.execute_sequence(['GLIF_GEN.01C', 'GLIF_HEL.04C'])
    pipeline = GlyphPipeline(nodes=[n1, n2], color_weights=[0.6, 0.4], sigma_field=np.random.rand(64, 64))
    result = pipeline.combine()
    bridge = SymbolicBridge(sigma_scalar=result['coherence'])
    color = bridge.glyph_color(result['coherence'])
    print('Pipeline summary:', result['summary'])
    print('Coherence:', round(result['coherence'], 4), '→ Color:', color)