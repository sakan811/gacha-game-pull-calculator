"""Implements the standard banner probability calculation strategy."""

from typing import Dict, Any
import numpy as np

from core.strategy import CalculationStrategy, CalculationResult
from core.common.errors import CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)


class StandardCalculationStrategy(CalculationStrategy):
    """Standard implementation of banner probability calculations."""

    def calculate(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate banner probabilities using standard pity system.

        Args:
            params: Dictionary containing calculation parameters

        Returns:
            CalculationResult containing probabilities

        Raises:
            CalculationError: If calculation fails
        """
        try:
            base_rate = float(params["base_rate"])
            hard_pity = int(params["hard_pity"])
            soft_pity_start = int(params["soft_pity_start"])
            rate_increase = float(params["rate_increase"])

            # Calculate probabilities
            pity_range = range(1, hard_pity + 1)
            raw_probs = [
                min(
                    1.0, base_rate * (1 + max(0, (i - soft_pity_start) * rate_increase))
                )
                for i in pity_range
            ]

            # Calculate first 5* probabilities
            not_yet_pulled = 1.0
            first_5star_probs = []
            for p in raw_probs:
                first_5star_probs.append(not_yet_pulled * p)
                not_yet_pulled *= 1 - p

            # Calculate cumulative probabilities
            cumulative_probs = np.cumsum(first_5star_probs)

            return CalculationResult(
                raw_probabilities=np.array(raw_probs),
                first_5star_prob=np.array(first_5star_probs),
                cumulative_prob=cumulative_probs,
                metadata={
                    "base_rate": base_rate,
                    "hard_pity": hard_pity,
                },
            )

        except Exception as e:
            logger.error(f"Calculation error: {str(e)}")
            raise CalculationError(f"Failed to calculate probabilities: {str(e)}")
