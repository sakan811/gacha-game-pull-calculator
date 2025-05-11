"""Calculation strategy interface and result types."""

from abc import ABC, abstractmethod
from typing import Dict, Any, NamedTuple
from numpy import ndarray

from ..common.errors import ValidationError
from ..common.logging import get_logger

logger = get_logger(__name__)


class CalculationResult(NamedTuple):
    """Container for calculation results with built-in validation."""

    raw_probabilities: ndarray
    first_5star_prob: ndarray
    cumulative_prob: ndarray
    metadata: Dict[str, Any]

    def validate(self) -> bool:
        """Validate calculation results.

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        if not all(
            isinstance(arr, ndarray)
            for arr in [
                self.raw_probabilities,
                self.first_5star_prob,
                self.cumulative_prob,
            ]
        ):
            raise ValidationError("All probability arrays must be numpy arrays")

        if not all(
            len(arr) > 0
            for arr in [
                self.raw_probabilities,
                self.first_5star_prob,
                self.cumulative_prob,
            ]
        ):
            raise ValidationError("All probability arrays must be non-empty")

        if not all(
            0 <= prob <= 1
            for arr in [
                self.raw_probabilities,
                self.first_5star_prob,
                self.cumulative_prob,
            ]
            for prob in arr
        ):
            raise ValidationError("All probabilities must be between 0 and 1")

        return True


class CalculationStrategy(ABC):
    """Interface for probability calculation strategies."""

    @abstractmethod
    def calculate(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate banner probabilities.

        Args:
            params: Calculation parameters

        Returns:
            Calculation results

        Raises:
            CalculationError: If calculation fails
        """
        pass
