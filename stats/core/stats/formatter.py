"""Module for formatting banner statistics results."""

from typing import List

from core.calculation.strategy import CalculationResult
from core.config.banner import BannerConfig
from core.common.errors import ValidationError
from core.common.logging import get_logger

logger = get_logger(__name__)


class StatsFormatter:
    """Formats banner statistics for output."""

    def __init__(self, config: BannerConfig):
        self.config = config

    def get_header(self) -> List[str]:
        """Get CSV header columns.

        Returns:
            List of column names
        """
        return [
            "Game",
            "Banner Type",
            "Roll Number",
            "Probability per Roll",
            "Cumulative Probability",
            "First 5 Star Probability",
        ]

    def validate_results(self, result: CalculationResult) -> None:
        """Validate calculation results before formatting.

        Args:
            result: Calculation results to validate

        Raises:
            ValidationError: If results are invalid
        """
        if (
            len(result.raw_probabilities)
            != len(result.cumulative_prob)
            != len(result.first_5star_prob)
        ):
            raise ValidationError("Probability arrays must be the same length")

    def format_number(self, value: float) -> str:
        """Format a number for CSV output.

        Args:
            value: Number to format

        Returns:
            Formatted string representation
        """
        return f"{value:.6f}"

    def format_results(self, results: CalculationResult) -> List[List[str]]:
        """Format calculation results.

        Args:
            results: Calculation results to format

        Returns:
            List of formatted rows
        """
        formatted_rows = []
        for i in range(len(results.raw_probabilities)):
            formatted_rows.append(
                [
                    str(i + 1),
                    f"{results.raw_probabilities[i]:.6f}",
                    f"{results.first_5star_prob[i]:.6f}",
                    f"{results.cumulative_prob[i]:.6f}",
                ]
            )
        return formatted_rows

    def format_metadata(self, results: CalculationResult) -> List[str]:
        """Format calculation metadata.

        Args:
            results: Calculation results containing metadata

        Returns:
            List of formatted metadata strings
        """
        return [
            f"Game: {self.config.game_name}",
            f"Banner Type: {self.config.banner_type}",
            f"Base Rate: {self.config.base_rate}",
            *[f"{k}: {v}" for k, v in results.metadata.items()],
        ]

    def format_rows(self, result: CalculationResult) -> List[List[str]]:
        """Format calculation results into rows.

        Args:
            result: Calculation results to format

        Returns:
            List of formatted data rows

        Raises:
            ValidationError: If results are invalid
        """
        try:
            self.validate_results(result)
            rows = []

            for i in range(len(result.raw_probabilities)):
                rows.append(
                    [
                        self.config.game_name,
                        self.config.banner_type,
                        str(i + 1),
                        self.format_number(result.raw_probabilities[i]),
                        self.format_number(result.cumulative_prob[i]),
                        self.format_number(result.first_5star_prob[i]),
                    ]
                )

            return rows

        except Exception as e:
            logger.error(f"Failed to format rows: {str(e)}")
            raise ValidationError(f"Failed to format calculation results: {str(e)}")
