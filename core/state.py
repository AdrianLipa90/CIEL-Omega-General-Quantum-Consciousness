from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.base import BaseCIELModule
from config import (
    PhysicalConstants,
    MathematicalConstants,
    ModelTuningParameters,
    PhysicalAliasView,
    TuningAliasView
)


@dataclass
class CoreStateModule(BaseCIELModule):
    """Core state module for CIEL.

    Manages:
    - Physical constants (phys)
    - Mathematical constants (math)
    - Tuning parameters (tuning)
    - Aliases for backward compatibility (phys_alias, tuning_alias)
    - Internal state storage

    This is a central module that serves as a reference for other
    subsystems (waves, memory, intention operator, etc.).
    """

    # Core components
    phys: PhysicalConstants = field(init=False)
    math: MathematicalConstants = field(init=False)
    tuning: ModelTuningParameters = field(init=False)

    # Alias views for backward compatibility
    phys_alias: PhysicalAliasView = field(init=False)
    tuning_alias: TuningAliasView = field(init=False)
    
    # Internal state storage
    internal_state: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize the core state components."""
        super().__post_init__()
        
        # Initialize core components
        self.phys = PhysicalConstants()
        self.math = MathematicalConstants()
        self.tuning = ModelTuningParameters()
        
        # Set up alias views
        self.phys_alias = PhysicalAliasView(self.phys)
        self.tuning_alias = TuningAliasView(self.tuning)
        
        # Log initialization
        self.kernel.logger.info(f"Initialized CoreStateModule: {self.name}")

    def step(self, dt: float) -> None:
        """Perform a single time step update.
        
        This method can be extended to include:
        - Field temperature updates
        - Coherence metrics
        - Other time-dependent state changes
        
        Args:
            dt: Time step in seconds
        """
        # Core state doesn't need to do anything on each step by default
        pass

    def get_state(self) -> dict[str, Any]:
        """Get the current state as a dictionary.
        
        Returns:
            Dictionary containing the current state with physical constants,
            mathematical constants, tuning parameters, and internal state.
        """
        return {
            "phys": {k: v for k, v in self.phys.__dict__.items() if not k.startswith("_")},
            "math": {k: v for k, v in self.math.__dict__.items() if not k.startswith("_")},
            "tuning": {k: v for k, v in self.tuning.__dict__.items() if not k.startswith("_")},
            "internal": dict(self.internal_state)
        }

    def update_state(self, updates: dict[str, Any]) -> None:
        """Update the state with new values.
        
        Args:
            updates: Dictionary containing updates to apply. Can include:
                - "phys": Updates to physical constants
                - "math": Updates to mathematical constants
                - "tuning": Updates to tuning parameters
                - "internal": Updates to internal state
        """
        for component, values in updates.items():
            if component == "internal":
                self.internal_state.update(values)
            elif hasattr(self, component):
                component_obj = getattr(self, component)
                for key, value in values.items():
                    if hasattr(component_obj, key):
                        setattr(component_obj, key, value)
                    else:
                        self.kernel.logger.warning(
                            f"Invalid key '{key}' for component '{component}'"
                        )
            else:
                self.kernel.logger.warning(f"Invalid component: {component}")

    def reset(self) -> None:
        """Reset the state to initial values.
        
        This will reinitialize all constants and clear the internal state.
        """
        self.phys = PhysicalConstants()
        self.math = MathematicalConstants()
        self.tuning = ModelTuningParameters()
        self.internal_state.clear()
        self.kernel.logger.info(f"Reset CoreStateModule: {self.name}")
        
        # Initialize some default internal state values
        self.internal_state.update({
            "t": 0.0,  # Time counter in natural units
            "temperature": 0.0,  # Field temperature
            "coherence": 1.0  # Coherence metric
        })
