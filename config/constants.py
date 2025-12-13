"""Constants and configuration for the CIEL system.

This module contains physical constants, mathematical constants,
and tunable parameters used throughout the CIEL system.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PhysicalConstants:
    """Physical constants used throughout the CIEL system."""
    # Speed of light in m/s
    c: float = 299_792_458.0
    # Planck's constant in J·s
    h: float = 6.62607015e-34
    # Reduced Planck constant in J·s
    hbar: float = 1.054571817e-34
    # Gravitational constant in m³·kg⁻¹·s⁻²
    G: float = 6.67430e-11
    k_B: float = 1.380649e-23
    eps0: float = 8.8541878128e-12
    mu_0: float = 1.25663706212e-06
    Lp: float = 1.616255e-35
    tp: float = 5.391247e-44
    mp: float = 2.176434e-08
    schumann_base_freq: float = 7.83


@dataclass
class MathematicalConstants:
    """Mathematical constants used throughout the CIEL system."""
    # Pi
    pi: float = 3.141592653589793
    # Euler's number
    e: float = 2.718281828459045
    # Golden ratio
    phi: float = 1.618033988749895
    EULER_MASCHERONI: float = 0.5772156649
    HOLOGRAPHIC_RATIO: float = 0.123456789
    LAMBDA_ZETA: float = 0.146


@dataclass
class ModelTuningParameters:
    """Tunable parameters for the CIEL model."""
    # Time step for simulation
    time_step: float = 0.01
    # Number of dimensions
    dimensions: int = 4
    # Precision for numerical calculations
    precision: float = 1e-10
    lambda_1: float = 0.1
    lambda_2: float = 0.05
    lambda_3: float = 0.2
    alpha: float = 0.01
    beta: float = 0.1
    eta: float = 0.001
    gamma: float = 0.02
    xi: float = 1.0
    KAPPA_MEMORY: float = 0.05
    TAU_RECALL: float = 0.1
    LIPA_CONSTANT: float = 0.474812
    MAX_COHERENCE: float = 0.751234
    ETHICAL_BOUND: float = 0.9
    SYMBOLIC_COUPLING: float = 0.856234
    TEMPORAL_FLOW: float = 0.345123
    RESONANCE_QUANTUM: float = 0.634567
    ENTANGLEMENT_STRENGTH: float = 0.723456
    INFORMATION_PRESERVATION: float = 0.998765
    OMEGA_LIFE: float = 0.786


@dataclass
class PhysicalAliasView:
    """View for physical constant aliases."""
    def __init__(self, constants: PhysicalConstants):
        self._constants = constants
    
    @property
    def c(self) -> float:
        return self._constants.c
    
    @property
    def h(self) -> float:
        return self._constants.h

    @property
    def h_bar(self) -> float:
        return self._constants.hbar

    @property
    def epsilon_0(self) -> float:
        return self._constants.eps0

    @property
    def L_p(self) -> float:
        return self._constants.Lp

    @property
    def L_planck(self) -> float:
        return self._constants.Lp

    @property
    def T_p(self) -> float:
        return self._constants.tp

    @property
    def t_planck(self) -> float:
        return self._constants.tp

    @property
    def M_p(self) -> float:
        return self._constants.mp

    @property
    def m_planck(self) -> float:
        return self._constants.mp


@dataclass
class TuningAliasView:
    """View for tuning parameter aliases."""
    def __init__(self, params: ModelTuningParameters):
        self._params = params
    
    @property
    def dt(self) -> float:
        return self._params.time_step

    @property
    def lam1(self) -> float:
        return self._params.lambda_1

    @property
    def lam2(self) -> float:
        return self._params.lambda_2

    @property
    def lam3(self) -> float:
        return self._params.lambda_3

    @property
    def INTENTION_GENERATOR(self) -> float:
        return self._params.xi

    @property
    def SCHRODINGER_PRIMORDIAL(self) -> float:
        return self._params.xi

    @property
    def E_BOUND(self) -> float:
        return self._params.ETHICAL_BOUND

    @property
    def life_threshold(self) -> float:
        return self._params.ETHICAL_BOUND

    @property
    def ALPHA_C(self) -> float:
        return self._params.LIPA_CONSTANT

    @property
    def CONSCIOUSNESS_QUANTUM(self) -> float:
        return self._params.LIPA_CONSTANT

    @property
    def LAMBDA(self) -> float:
        return self._params.LIPA_CONSTANT

    @property
    def BETA_S(self) -> float:
        return self._params.SYMBOLIC_COUPLING

    @property
    def GAMMA_T(self) -> float:
        return self._params.TEMPORAL_FLOW

    @property
    def DELTA_R(self) -> float:
        return self._params.RESONANCE_QUANTUM

    @property
    def GAMMA_MAX(self) -> float:
        return self._params.MAX_COHERENCE

    @property
    def LAMBDA_I(self) -> float:
        return self._params.ENTANGLEMENT_STRENGTH

    @property
    def OMEGA_STRUCTURE(self) -> float:
        return self._params.OMEGA_LIFE
