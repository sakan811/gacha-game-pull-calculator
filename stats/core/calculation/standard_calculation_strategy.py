"""Implements the standard banner probability calculation strategy."""

from typing import Dict, Any, List
import numpy as np

from core.calculation.strategy import CalculationStrategy, CalculationResult
from core.common.errors import CalculationError, ValidationError
from core.common.logging import get_logger

logger = get_logger(__name__)


class StandardCalculationStrategy(CalculationStrategy):
    """Standard implementation of banner probability calculations."""

    def calculate(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate banner probabilities using standard pity system.

        Args:
            params: Dictionary containing:
                - base_rate: Base probability rate (float)
                - hard_pity: Maximum pity value (int)
                - soft_pity_start: Start of soft pity (int)
                - rate_increase: Rate increase per roll after soft pity (float)

        Returns:
            CalculationResult with calculation outcomes

        Raises:
            ValidationError: If required parameters are missing or invalid
            CalculationError: If calculation fails
        """
        try:
            try:
                base_rate = float(params["base_rate"])
                hard_pity = int(params["hard_pity"])
                soft_pity_start = int(params["soft_pity_start"])
                rate_increase = float(params["rate_increase"])
            except (KeyError, ValueError, TypeError) as e:
                raise ValidationError(f"Invalid parameter value: {str(e)}")

            if not 0 < base_rate <= 1:
                raise ValidationError("Base rate must be between 0 and 1")
            if not 0 < hard_pity <= 100:
                raise ValidationError("Hard pity must be between 1 and 100")
            if not 0 < soft_pity_start < hard_pity:
                raise ValidationError("Soft pity must be between 1 and hard pity")
            if not 0 <= rate_increase <= 1:
                raise ValidationError("Rate increase must be between 0 and 1")

            pity_range = range(1, hard_pity + 1)
            rolls = list(pity_range)

            raw_probs = [
                min(
                    1.0, base_rate * (1 + max(0, (i - soft_pity_start) * rate_increase))
                )
                for i in rolls
            ]
            first_5star_probs = self._calculate_first_5star_probabilities(raw_probs)
            cumulative_probs = self._calculate_cumulative_probabilities(raw_probs)

            metadata = {
                "base_rate": base_rate,
                "hard_pity": hard_pity,
                "soft_pity_start": soft_pity_start,
                "rate_increase": rate_increase,
                "total_rolls": len(rolls),
            }

            result = CalculationResult(
                raw_probabilities=np.array(raw_probs),
                first_5star_prob=np.array(first_5star_probs),
                cumulative_prob=np.array(cumulative_probs),
                metadata=metadata,
            )

            # Validate the result before returning
            result.validate()
            return result

        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Calculation error: {str(e)}")
            raise CalculationError(f"Probability calculation failed: {str(e)}")

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
