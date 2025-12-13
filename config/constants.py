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


@dataclass
class MathematicalConstants:
    """Mathematical constants used throughout the CIEL system."""
    # Pi
    pi: float = 3.141592653589793
    # Euler's number
    e: float = 2.718281828459045
    # Golden ratio
    phi: float = 1.618033988749895


@dataclass
class ModelTuningParameters:
    """Tunable parameters for the CIEL model."""
    # Time step for simulation
    time_step: float = 0.01
    # Number of dimensions
    dimensions: int = 4
    # Precision for numerical calculations
    precision: float = 1e-10


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


@dataclass
class TuningAliasView:
    """View for tuning parameter aliases."""
    def __init__(self, params: ModelTuningParameters):
        self._params = params
    
    @property
    def dt(self) -> float:
        return self._params.time_step
