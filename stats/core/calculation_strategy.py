"""Defines the interface for probability calculation strategies."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class CalculationStrategy(ABC):
    """Base class for probability calculation strategies."""

    @abstractmethod
    def calculate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate probabilities based on given parameters.

        Args:
            params: Dictionary containing calculation parameters.

        Returns:
            Dictionary containing calculation results.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        pass
