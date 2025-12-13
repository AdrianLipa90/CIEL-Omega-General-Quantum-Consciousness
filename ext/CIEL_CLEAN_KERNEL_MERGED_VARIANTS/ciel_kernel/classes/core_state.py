from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..orchestrator import CIELKernel
from ..constants import PhysicalConstants, MathematicalConstants, ModelTuningParameters
from ..constants import PhysicalAliasView, TuningAliasView
from .base import BaseCIELModule


@dataclass
class CoreStateModule(BaseCIELModule):
    """Podstawowy moduł stanu CIEL.

    Zna:
    - stałe fizyczne (phys),
    - stałe matematyczne (math),
    - parametry strojenia (tuning),
    - aliasy dla starych nazw (phys_alias, tuning_alias).

    To jest „centralny” moduł, który może być punktem odniesienia dla innych
    podsystemów (fal, pamięci, operatora intencji itd.).
    """

    phys: PhysicalConstants = field(init=False)
    math: MathematicalConstants = field(init=False)
    tuning: ModelTuningParameters = field(init=False)

    phys_alias: PhysicalAliasView = field(init=False)
    tuning_alias: TuningAliasView = field(init=False)

    internal_state: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.phys = self.kernel.phys
        self.math = self.kernel.math
        self.tuning = self.kernel.tuning
        self.phys_alias = PhysicalAliasView(self.phys)
        self.tuning_alias = TuningAliasView(self.tuning)

        # Przykładowa inicjalizacja stanu z użyciem zunifikowanych parametrów:
        self.internal_state["LIPA_CONSTANT"] = self.tuning.LIPA_CONSTANT
        self.internal_state["ETHICAL_BOUND"] = self.tuning.ETHICAL_BOUND

    def step(self, dt: float) -> None:
        """Krok aktualizacji stanu.

        Na razie symboliczny: pokazuje, jak korzystać z parametrów.
        Tu w przyszłości można wpiąć:
        - aktualizację „temperatury” pola,
        - metryki koherencji,
        - wskaźniki nieliniowości / krytyczności.
        """
        # Przykład: możemy tu np. przechowywać licznik czasu w jednostkach naturalnych.
        t = self.internal_state.get("t", 0.0)
        self.internal_state["t"] = t + dt
