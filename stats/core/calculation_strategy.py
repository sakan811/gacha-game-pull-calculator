"""Defines the interface for probability calculation strategies."""

from abc import ABC, abstractmethod
from typing import Dict, Any, NamedTuple
import numpy as np
from numpy.typing import NDArray


class CalculationError(Exception):
    """Base error for calculation failures."""

    pass


class ValidationError(CalculationError):
    """Validation error in calculations."""

    pass


class ConfigurationError(CalculationError):
    """Configuration error in banner setup."""

    pass


class CalculationResult(NamedTuple):
    """Container for calculation results with built-in validation."""

    raw_probabilities: NDArray[np.float64]
    first_5star_prob: NDArray[np.float64]
    cumulative_prob: NDArray[np.float64]
    metadata: Dict[str, Any]

    def validate(self) -> bool:
        """Validate calculation results."""
        return (
            self.raw_probabilities is not None
            and self.first_5star_prob is not None
            and self.cumulative_prob is not None
            and len(self.raw_probabilities) > 0
            and len(self.first_5star_prob) == len(self.raw_probabilities)
            and len(self.cumulative_prob) == len(self.raw_probabilities)
        )


class CalculationStrategy(ABC):
    """Base class for probability calculation strategies."""

    @abstractmethod
    def calculate(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate probabilities based on given parameters.

        Args:
            params: Dictionary containing calculation parameters.

        Returns:
            CalculationResult containing calculation results and metadata.

        Raises:
            ValidationError: If parameters are invalid.
            CalculationError: If calculation fails.
        """
        pass
