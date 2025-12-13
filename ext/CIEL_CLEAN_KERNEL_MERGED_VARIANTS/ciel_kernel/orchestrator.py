from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, runtime_checkable

from .constants import PhysicalConstants, MathematicalConstants, ModelTuningParameters


@runtime_checkable
class CIELModule(Protocol):
    """Interfejs dla modułu kernela CIEL.

    Każdy moduł:
    - zna referencję do głównego kernela,
    - może zostać wywołany w kroku czasowym `step(dt)`,
    - może aktualizować wewnętrzny stan.
    """

    name: str

    def step(self, dt: float) -> None:
        ...


@dataclass
class CIELKernel:
    """Główny orkiestrator CIEL/Ω.

    Łączy:
    - stałe fizyczne i matematyczne,
    - parametry strojenia,
    - zarejestrowane moduły (podsystemy kernela).

    To jest lekki, „czysty” rdzeń, na który można nakładać kolejne warstwy:
    - pola falowe,
    - pamięć,
    - operator intencji,
    - integrację z LLM / dashboardem.
    """

    phys: PhysicalConstants = field(default_factory=PhysicalConstants)
    math: MathematicalConstants = field(default_factory=MathematicalConstants)
    tuning: ModelTuningParameters = field(default_factory=ModelTuningParameters)

    modules: Dict[str, CIELModule] = field(default_factory=dict)

    def register_module(self, module: CIELModule, *, override: bool = False) -> None:
        """Rejestruje moduł w kernelu.

        :param module: instancja implementująca interfejs CIELModule
        :param override: czy nadpisać istniejący moduł o tej samej nazwie
        """
        if not isinstance(module, CIELModule):
            # Prosty runtime guard – nie łapiemy wszystkiego, ale ograniczamy wtopy.
            raise TypeError(f"Module {module!r} nie implementuje interfejsu CIELModule")

        if module.name in self.modules and not override:
            raise ValueError(f"Moduł '{module.name}' jest już zarejestrowany")

        self.modules[module.name] = module

    def get_module(self, name: str) -> Optional[CIELModule]:
        """Zwraca moduł o zadanej nazwie (lub None, jeśli nie istnieje)."""
        return self.modules.get(name)

    def step(self, dt: float) -> None:
        """Wykonuje jeden krok czasowy dla wszystkich modułów.

        `dt` możesz traktować jako:
        - krok czasowy w jednostkach naturalnych,
        - krok iteracji / epoki w sensie optymalizacji,
        - jednostkę „tiknięcia” pola świadomości.
        """
        for module in list(self.modules.values()):
            module.step(dt)
