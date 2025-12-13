import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg, integrate, special, ndimage
from scipy.interpolate import RectBivariateSpline
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any, Union
import warnings
import numpy.typing as npt
from sympy import isprime

class CompleteUnifiedEvolutionEngine:

    def __init__(self, spacetime_shape: Tuple[int, int, int]=(32, 32, 20), grid_4d_shape: Tuple[int, int, int, int]=(8, 8, 8, 6)):
        self.constants = UnifiedCIELConstants()
        self.fields = UnifiedSevenFundamentalFields(self.constants, spacetime_shape)
        self.lagrangian = UnifiedCIELLagrangian(self.constants, self.fields)
        self.info_dynamics = UnifiedInformationDynamics(self.constants, self.fields)
        self.engine_4d = UniversalLawEngine4D(grid_4d_shape)
        self.lie4_constants = Lie4Constants()
        self.lie4 = Lie4Algebra(self.lie4_constants)
        self.step = 0
        self.history = {'energy': [], 'coherence': [], 'resonance': [], 'creation': []}

    def evolution_step(self, dt: float=0.01) -> Dict[str, float]:
        self.step += 1
        state_4d = self.engine_4d.cosmic_evolution_step_4d(dt)
        self.fields.update_from_4d_engine(self.engine_4d)
        self.info_dynamics.evolve_information_field(dt)
        L = self.lagrangian.compute_lagrangian_density()
        total_action = np.sum(np.real(L)) * dt
        metrics = {'step': self.step, 'action': float(total_action), 'energy': float(np.mean(np.abs(L))), 'quantum_coherence': state_4d['quantum_coherence'], 'universal_resonance': state_4d['universal_resonance'], 'creation_intensity': state_4d['creation_intensity'], 'field_norm_psi': float(np.linalg.norm(self.fields.psi)), 'field_norm_I': float(np.linalg.norm(self.fields.I_field))}
        self.history['energy'].append(metrics['energy'])
        self.history['coherence'].append(metrics['quantum_coherence'])
        self.history['resonance'].append(metrics['universal_resonance'])
        self.history['creation'].append(metrics['creation_intensity'])
        return metrics

    def run_simulation(self, n_steps: int=100, dt: float=0.01) -> List[Dict]:
        results = []
        print(f'\nStarting CIEL/0 simulation with {n_steps} steps...')
        print('=' * 60)
        for i in range(n_steps):
            metrics = self.evolution_step(dt)
            results.append(metrics)
            if i % 10 == 0:
                print(f"Step {i}/{n_steps}: E={metrics['energy']:.6f}, Q={metrics['quantum_coherence']:.4f}, R={metrics['universal_resonance']:.4f}")
        print('=' * 60)
        print(f'✅ Simulation completed successfully!')
        return results