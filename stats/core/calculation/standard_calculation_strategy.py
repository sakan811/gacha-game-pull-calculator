"""Implements the standard banner probability calculation strategy."""

from typing import Dict, Any, List

from core.calculation_strategy import CalculationStrategy
from core.banner import BannerConfig


class StandardCalculationStrategy(CalculationStrategy):
    """Standard implementation of banner probability calculations."""

    def calculate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate banner probabilities using standard pity system.

        Args:
            params: Dictionary containing:
                - config: BannerConfig instance
                - pity_range: Range of pity values to calculate

        Returns:
            Dictionary containing calculation results with keys:
                - rolls: List of roll numbers
                - raw_probabilities: Base probability per roll
                - cumulative_probabilities: Cumulative chance
                - first_5_star_probabilities: Chance of first 5-star

        Raises:
            ValueError: If required parameters are missing
        """
        config = params.get("config")
        pity_range = params.get("pity_range", range(1, 91))

        if not isinstance(config, BannerConfig):
            raise ValueError("Valid BannerConfig required")

        rolls = list(pity_range)
        raw_probs = self._calculate_raw_probabilities(config, rolls)
        first_5star_probs = self._calculate_first_5star_probabilities(raw_probs)
        cumulative_probs = self._calculate_cumulative_probabilities(raw_probs)

        return {
            "rolls": rolls,
            "raw_probabilities": raw_probs,
            "first_5_star_probabilities": first_5star_probs,
            "cumulative_probabilities": cumulative_probs,
        }

    def _calculate_raw_probabilities(
        self, config: BannerConfig, rolls: List[int]
    ) -> List[float]:
        """Calculate raw probability for each roll.

        Args:
            config: Banner configuration
            rolls: List of roll numbers

        Returns:
            List of probabilities per roll
        """
        base_rate = config.base_rate
        pity_starts = config.pity_starts
        max_pity = config.max_pity

        return [
            min(
                1.0,
                base_rate * (1 + max(0, (i - pity_starts) / (max_pity - pity_starts))),
            )
            for i in rolls
        ]

    def _calculate_first_5star_probabilities(
        self, raw_probs: List[float]
    ) -> List[float]:
        """Calculate probability of getting first 5-star at each roll.

        Args:
            raw_probs: List of raw probabilities per roll

        Returns:
            List of probabilities for first 5-star
        """
        result = []
        cumulative_fail = 1.0

        for prob in raw_probs:
            prob_here = cumulative_fail * prob
            cumulative_fail *= 1 - prob
            result.append(prob_here)

        return result

    def _calculate_cumulative_probabilities(
        self, raw_probs: List[float]
    ) -> List[float]:
        """Calculate cumulative probability of getting at least one 5-star.

        Args:
            raw_probs: List of raw probabilities per roll

        Returns:
            List of cumulative probabilities
        """
        result = []
        cumulative_fail = 1.0

        for prob in raw_probs:
            cumulative_fail *= 1 - prob
            result.append(1 - cumulative_fail)

        return result
