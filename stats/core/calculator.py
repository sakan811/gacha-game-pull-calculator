"""Calculator module for banner probability calculations.

This module provides the calculator class for banner probabilities.
It handles the core probability calculations for gacha banners including pity systems.
"""

import numpy as np

from core.config.banner import BannerConfig
from core.common.errors import ConfigurationError, CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)


class CalculationResult:
    """Container for calculation results."""

    def __init__(
        self,
        raw_probabilities: np.ndarray,
        first_5star_prob: np.ndarray,
        cumulative_prob: np.ndarray,
    ):
        self.raw_probabilities = raw_probabilities
        self.first_5star_prob = first_5star_prob
        self.cumulative_prob = cumulative_prob


class ProbabilityCalculator:
    """Handles probability calculations for banners."""

    def __init__(self, config: BannerConfig) -> None:
        if not config:
            raise ConfigurationError("Banner configuration is required")
        self.config = config

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
            # Use config parameters for soft pity and rate increase
            probs = np.full(max_rolls, self.config.base_rate, dtype=np.float64)
            soft_pity = self.config.soft_pity_start_after
            hard_pity = self.config.hard_pity
            rate_increase = self.config.rate_increase

            # Apply soft pity
            for i in range(soft_pity - 1, min(hard_pity, max_rolls)):
                increased_rate = min(
                    1.0, self.config.base_rate + (i - (soft_pity - 1)) * rate_increase
                )
                probs[i] = increased_rate

            # Guarantee at hard pity
            if hard_pity <= max_rolls:
                probs[hard_pity - 1] = 1.0

            # First 5-star probability per roll
            not_pulled_yet = np.cumprod(1 - probs)
            first_5star = probs * np.concatenate(([1.0], not_pulled_yet[:-1]))

            # Cumulative probability
            cumulative = 1.0 - not_pulled_yet

            return CalculationResult(
                raw_probabilities=probs,
                first_5star_prob=first_5star,
                cumulative_prob=cumulative,
            )
        except Exception as e:
            logger.error(f"Calculation failed: {str(e)}", exc_info=True)
            raise CalculationError(f"Failed to calculate probabilities: {str(e)}")
