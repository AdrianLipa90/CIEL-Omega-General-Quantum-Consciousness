from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

# Define the CIELKernel and CIELModule interfaces
class CIELKernel(Protocol):
    """Protocol defining the CIEL Kernel interface."""
    pass

class CIELModule(Protocol):
    """Protocol defining the base module interface."""
    kernel: CIELKernel
    name: str
    config: dict[str, Any]
    
    def step(self, dt: float) -> None:
        """Perform a single time step update."""
        ...


@dataclass
class BaseCIELModule(CIELModule):
    """Base class for all CIEL modules.

    This provides a convenient skeleton for concrete modules.
    Implements the CIELModule interface from the orchestrator.
    """

    kernel: CIELKernel
    name: str
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        return None

    def step(self, dt: float) -> None:
        """Default step implementation - to be overridden by subclasses.

        You can use this for:
        - State updates
        - Motion equation execution
        - Synchronization with other fields
        """
        # By default, do nothing - this is just a skeleton.
        return None
