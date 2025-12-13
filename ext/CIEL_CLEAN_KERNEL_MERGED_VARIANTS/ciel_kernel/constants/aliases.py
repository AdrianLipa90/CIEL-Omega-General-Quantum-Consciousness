# -*- coding: utf-8 -*-
"""Warstwa aliasów nazw stałych/hyperparametrów.

Zapewnia kompatybilność wsteczną dla dawnych nazw metryk,

mapując je na zunifikowane nazwy kanoniczne kernela CIEL/Ω.

"""

from dataclasses import dataclass
from typing import Dict

from .physical_math_constants import PhysicalConstants
from .tuning_parameters import ModelTuningParameters


PHYSICAL_ALIASES: Dict[str, str] = {'h_bar': 'hbar', 'epsilon_0': 'eps0', 'L_p': 'Lp', 'L_planck': 'Lp', 'T_p': 'tp', 't_planck': 'tp', 'M_p': 'mp', 'm_planck': 'mp'}
TUNING_ALIASES: Dict[str, str] = {'lam1': 'lambda_1', 'lam2': 'lambda_2', 'lam3': 'lambda_3', 'INTENTION_GENERATOR': 'xi', 'SCHRODINGER_PRIMORDIAL': 'xi', 'E_BOUND': 'ETHICAL_BOUND', 'life_threshold': 'ETHICAL_BOUND', 'ALPHA_C': 'LIPA_CONSTANT', 'CONSCIOUSNESS_QUANTUM': 'LIPA_CONSTANT', 'LAMBDA': 'LIPA_CONSTANT', 'BETA_S': 'SYMBOLIC_COUPLING', 'GAMMA_T': 'TEMPORAL_FLOW', 'DELTA_R': 'RESONANCE_QUANTUM', 'GAMMA_MAX': 'MAX_COHERENCE', 'LAMBDA_I': 'ENTANGLEMENT_STRENGTH', 'OMEGA_STRUCTURE': 'OMEGA_LIFE'}

@dataclass(frozen=True)
class PhysicalAliasView:
    """Dostęp do stałych fizycznych po dawnych nazwach aliasów.

    Np. h_bar → hbar, epsilon_0 → eps0, L_planck → Lp.

    """
    base: PhysicalConstants

    @property
    def h_bar(self) -> float:
        """Alias dla hbar."""
        return self.base.hbar

    @property
    def epsilon_0(self) -> float:
        """Alias dla eps0."""
        return self.base.eps0

    @property
    def L_p(self) -> float:
        """Alias dla Lp."""
        return self.base.Lp

    @property
    def L_planck(self) -> float:
        """Alias dla Lp."""
        return self.base.Lp

    @property
    def T_p(self) -> float:
        """Alias dla tp."""
        return self.base.tp

    @property
    def t_planck(self) -> float:
        """Alias dla tp."""
        return self.base.tp

    @property
    def M_p(self) -> float:
        """Alias dla mp."""
        return self.base.mp

    @property
    def m_planck(self) -> float:
        """Alias dla mp."""
        return self.base.mp

@dataclass
class TuningAliasView:
    """Dostęp do parametrów strojenia po dawnych nazwach aliasów.

    Np. lam1 → lambda_1, ALPHA_C/CONSCIOUSNESS_QUANTUM/LAMBDA → LIPA_CONSTANT itd.

    """
    base: ModelTuningParameters

    @property
    def lam1(self) -> float:
        """Alias dla lambda_1."""
        return self.base.lambda_1

    @property
    def lam2(self) -> float:
        """Alias dla lambda_2."""
        return self.base.lambda_2

    @property
    def lam3(self) -> float:
        """Alias dla lambda_3."""
        return self.base.lambda_3

    @property
    def INTENTION_GENERATOR(self) -> float:
        """Alias dla xi."""
        return self.base.xi

    @property
    def SCHRODINGER_PRIMORDIAL(self) -> float:
        """Alias dla xi."""
        return self.base.xi

    @property
    def E_BOUND(self) -> float:
        """Alias dla ETHICAL_BOUND."""
        return self.base.ETHICAL_BOUND

    @property
    def life_threshold(self) -> float:
        """Alias dla ETHICAL_BOUND."""
        return self.base.ETHICAL_BOUND

    @property
    def ALPHA_C(self) -> float:
        """Alias dla LIPA_CONSTANT."""
        return self.base.LIPA_CONSTANT

    @property
    def CONSCIOUSNESS_QUANTUM(self) -> float:
        """Alias dla LIPA_CONSTANT."""
        return self.base.LIPA_CONSTANT

    @property
    def LAMBDA(self) -> float:
        """Alias dla LIPA_CONSTANT."""
        return self.base.LIPA_CONSTANT

    @property
    def BETA_S(self) -> float:
        """Alias dla SYMBOLIC_COUPLING."""
        return self.base.SYMBOLIC_COUPLING

    @property
    def GAMMA_T(self) -> float:
        """Alias dla TEMPORAL_FLOW."""
        return self.base.TEMPORAL_FLOW

    @property
    def DELTA_R(self) -> float:
        """Alias dla RESONANCE_QUANTUM."""
        return self.base.RESONANCE_QUANTUM

    @property
    def GAMMA_MAX(self) -> float:
        """Alias dla MAX_COHERENCE."""
        return self.base.MAX_COHERENCE

    @property
    def LAMBDA_I(self) -> float:
        """Alias dla ENTANGLEMENT_STRENGTH."""
        return self.base.ENTANGLEMENT_STRENGTH

    @property
    def OMEGA_STRUCTURE(self) -> float:
        """Alias dla OMEGA_LIFE."""
        return self.base.OMEGA_LIFE

