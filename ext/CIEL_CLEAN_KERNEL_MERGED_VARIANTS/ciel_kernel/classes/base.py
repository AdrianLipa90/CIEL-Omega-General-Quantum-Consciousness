from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..orchestrator import CIELKernel, CIELModule


@dataclass
class BaseCIELModule:
    """Bazowa klasa modułu CIEL.

    To jest wygodny „szkielet” dla konkretnych modułów.
    Implementuje interfejs CIELModule z orkiestratora.
    """

    kernel: CIELKernel
    name: str
    config: dict[str, Any] = field(default_factory=dict)

    def step(self, dt: float) -> None:
        """Domyślna implementacja kroku – do nadpisania w subclass.

        Możesz traktować to jako:
        - miejsce na update stanu,
        - wykonywanie równania ruchu,
        - synchronizację z innymi polami.
        """
        # Domyślnie nic nie robi — to jest tylko szkielet.
        return None
