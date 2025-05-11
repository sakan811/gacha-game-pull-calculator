"""Calculator module for banner probability calculations.

This module provides the calculator class for banner probabilities.
It handles the core probability calculations for gacha banners including pity systems.
"""

from typing import Dict, Any
import numpy as np

from core.config.banner import BannerConfig
from core.common.errors import ConfigurationError, CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)


class ProbabilityCalculator:
    """Handles probability calculations for banners."""

    def __init__(self, config: BannerConfig) -> None:
        if not config:
            raise ConfigurationError("Banner configuration is required")
        self.config = config

    def calculate_probabilities(self, max_rolls: int = 180) -> Dict[str, Any]:
        """Calculate banner probabilities.

        Args:
            max_rolls: Maximum number of rolls to calculate for

        Returns:
            Dictionary with probability arrays and metadata

        Raises:
            CalculationError: If calculation fails
        """
        try:
            probs = np.zeros(max_rolls, dtype=np.float64)
            base_rate = self.config.base_rate
            for i in range(max_rolls):
                # Apply pity system
                if i >= 73:
                    base_rate = min(1.0, self.config.base_rate + (i - 72) * 0.06)
                probs[i] = base_rate

            n = len(probs)
            first_5star = np.zeros(n, dtype=np.float64)
            not_pulled_yet = 1.0
            for i in range(n):
                first_5star[i] = probs[i] * not_pulled_yet
                not_pulled_yet *= 1 - probs[i]

            cumulative = np.zeros(n, dtype=np.float64)
            not_pulled = 1.0
            for i in range(n):
                cumulative[i] = 1.0 - not_pulled
                not_pulled *= 1 - probs[i]

            return {
                "raw_probabilities": probs,
                "first_5star_prob": first_5star,
                "cumulative_prob": cumulative,
                "metadata": {
                    "max_rolls": max_rolls,
                    "banner_type": self.config.banner_type,
                    "base_rate": self.config.base_rate,
                },
            }
        except Exception as e:
            logger.error(f"Calculation failed: {str(e)}", exc_info=True)
            raise CalculationError(f"Failed to calculate probabilities: {str(e)}")
