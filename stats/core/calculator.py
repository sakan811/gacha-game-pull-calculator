"""Calculator module for banner probability calculations.

This module provides the calculator class for banner probabilities.
It handles the core probability calculations for gacha banners including pity systems.
"""

from typing import Dict, Any
import numpy as np
from numpy.typing import NDArray

from core.config.banner import BannerConfig
from core.common.errors import ConfigurationError, CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)

# Type aliases for improved readability
ProbabilityArray = NDArray[np.float64]
RollArray = NDArray[np.int64]


class CalculationResult:
    """Container for calculation results."""

    def __init__(
        self,
        raw_probabilities: ProbabilityArray,
        cumulative_prob: ProbabilityArray,
        first_5star_prob: ProbabilityArray,
        metadata: Dict[str, Any],
    ):
        self.raw_probabilities = raw_probabilities
        self.cumulative_prob = cumulative_prob
        self.first_5star_prob = first_5star_prob
        self.metadata = metadata


class ProbabilityCalculator:
    """Calculates banner probabilities including pity systems.

    Attributes:
        config: Banner configuration parameters
        rolls: Array of roll numbers from 1 to hard pity
    """

    def __init__(self, config: BannerConfig):
        """Initialize calculator with banner configuration.

        Args:
            config: Banner configuration parameters
        """
        self.config = config
        self.rolls = np.arange(1, config.hard_pity + 1, dtype=np.int64)
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate banner configuration.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if self.config.base_rate <= 0 or self.config.base_rate >= 1:
            raise ConfigurationError("Base rate must be between 0 and 1")
        if self.config.hard_pity <= self.config.soft_pity_start_after:
            raise ConfigurationError("Hard pity must be greater than soft pity start")
        if self.config.rate_increase < 0:
            raise ConfigurationError("Rate increase cannot be negative")

    def calculate(self) -> CalculationResult:
        """Calculate banner probabilities.

        Returns:
            CalculationResult containing probability arrays and metadata

        Raises:
            CalculationError: If calculation fails
        """
        try:
            # Calculate base probabilities
            probs = np.full_like(self.rolls, self.config.base_rate, dtype=np.float64)

            # Apply soft pity
            soft_pity_mask = self.rolls > self.config.soft_pity_start_after
            probs[soft_pity_mask] += self.config.rate_increase

            # Apply hard pity
            probs[self.config.hard_pity - 1] = 1.0

            # Calculate cumulative probability of not getting a 5-star
            not_gotten = np.cumprod(1 - probs).astype(np.float64)

            # Calculate probability of getting first 5-star on each roll
            first_5star = (probs * not_gotten).astype(np.float64)

            # Calculate cumulative probability of getting a 5-star
            cumulative = (1 - not_gotten).astype(np.float64)

            return CalculationResult(
                raw_probabilities=probs,
                cumulative_prob=cumulative,
                first_5star_prob=first_5star,
                metadata={
                    "banner_type": self.config.banner_type,
                    "total_probability": float(cumulative[-1]),
                },
            )

        except Exception as e:
            raise CalculationError(f"Failed to calculate probabilities: {e}") from e
