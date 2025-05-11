"""Module for formatting banner statistics results."""

from typing import List

from ..calculation.strategy import CalculationResult
from ..config.banner import BannerConfig
from ..common.logging import get_logger

logger = get_logger(__name__)


class StatsFormatter:
    """Formats banner statistics for output."""

    def __init__(self, config: BannerConfig):
        self.config = config

    def get_header(self) -> List[str]:
        """Get header row for formatted output.

        Returns:
            List of column headers
        """
        return [
            "Pulls",
            "Raw Probability",
            "First 5★ Probability",
            "Cumulative Probability",
        ]

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
