"""Calculator module for banner probability calculations.

This module provides the calculator class for banner probabilities.
It handles the core probability calculations for gacha banners including pity systems.
"""

from typing import Dict, Any, NamedTuple
from numpy.typing import NDArray
import numpy as np

from core.config.banner import BannerConfig
from core.common.errors import ConfigurationError, CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)

# Type aliases for improved readability
ProbabilityArray = NDArray[np.float64]
RollArray = NDArray[np.int64]


class CalculationResult(NamedTuple):
    """Container for calculation results with built-in validation."""

    raw_probabilities: NDArray[np.float64]
    first_5star_prob: NDArray[np.float64]
    cumulative_prob: NDArray[np.float64]
    metadata: Dict[str, Any]

    def validate(self) -> bool:
        """Validate probability arrays.

        Returns:
            bool: True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        arrays = [self.raw_probabilities, self.first_5star_prob, self.cumulative_prob]
        for arr in arrays:
            if not isinstance(arr, np.ndarray) or arr.size == 0:
                raise CalculationError("Empty or invalid probability array")
            if not np.all((arr >= 0) & (arr <= 1)):
                raise CalculationError("Probabilities must be between 0 and 1")
        return True


class ProbabilityCalculator:
    """Handles probability calculations for banners."""

    def __init__(self, config: BannerConfig) -> None:
        """Initialize calculator with banner configuration.

        Args:
            config: Banner configuration parameters

        Raises:
            ConfigurationError: If configuration is invalid
        """
        self.config = config
        self.validate_config()

    def validate_config(self) -> None:
        """Validate calculator configuration.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if not self.config:
            raise ConfigurationError("Banner configuration is required")

    def calculate_probabilities(self, max_rolls: int = 180) -> CalculationResult:
        """Calculate banner probabilities.

        Args:
            max_rolls: Maximum number of rolls to calculate for

        Returns:
            CalculationResult with probability arrays

        Raises:
            CalculationError: If calculation fails
        """
        try:
            # Calculate raw probabilities first
            raw_probs = self._calculate_raw_probabilities(max_rolls)

            # Calculate first 5-star probabilities
            first_5star = self._calculate_first_5star_prob(raw_probs)

            # Calculate cumulative probabilities
            cumulative = self._calculate_cumulative_prob(raw_probs)

            result = CalculationResult(
                raw_probabilities=raw_probs,
                first_5star_prob=first_5star,
                cumulative_prob=cumulative,
                metadata={
                    "max_rolls": max_rolls,
                    "banner_type": self.config.banner_type,
                    "base_rate": self.config.base_rate,
                },
            )
            result.validate()
            return result

        except Exception as e:
            logger.error(f"Calculation failed: {str(e)}", exc_info=True)
            raise CalculationError(f"Failed to calculate probabilities: {str(e)}")

    def _calculate_raw_probabilities(self, max_rolls: int) -> NDArray[np.float64]:
        """Calculate raw probabilities for each roll.

        Args:
            max_rolls: Maximum number of rolls

        Returns:
            Array of probabilities per roll
        """
        probs = np.zeros(max_rolls, dtype=np.float64)
        base_rate = self.config.base_rate

        for i in range(max_rolls):
            # Apply pity system
            if i >= 73:  # Soft pity
                base_rate = min(1.0, base_rate + (i - 72) * 0.06)
            probs[i] = base_rate

        return probs

    def _calculate_first_5star_prob(self, raw_probs: NDArray[np.float64]) -> NDArray[np.float64]:
        """Calculate probability of first 5-star at each roll.

        Args:
            raw_probs: Raw probabilities per roll

        Returns:
            Array of first 5-star probabilities
        """
        n = len(raw_probs)
        first_5star = np.zeros(n, dtype=np.float64)

        not_pulled_yet = 1.0
        for i in range(n):
            first_5star[i] = raw_probs[i] * not_pulled_yet
            not_pulled_yet *= (1 - raw_probs[i])

        return first_5star

    def _calculate_cumulative_prob(self, raw_probs: NDArray[np.float64]) -> NDArray[np.float64]:
        """Calculate cumulative probability of pulling a 5-star.

        Args:
            raw_probs: Raw probabilities per roll

        Returns:
            Array of cumulative probabilities
        """
        n = len(raw_probs)
        cumulative = np.zeros(n, dtype=np.float64)

        not_pulled = 1.0
        for i in range(n):
            cumulative[i] = 1.0 - not_pulled
            not_pulled *= (1 - raw_probs[i])

        return cumulative
