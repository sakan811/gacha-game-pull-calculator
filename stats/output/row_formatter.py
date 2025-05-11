"""Handles formatting of banner data into CSV rows."""

from typing import List, Tuple, Generator, Union
from core.banner import BannerConfig
from core.calculation_strategy import CalculationResult


class BannerRowFormatter:
    """Formats banner data into CSV rows."""

    def __init__(self, config: BannerConfig):
        self.config = config

    def get_header(self) -> List[str]:
        """Generate the CSV header row.

        Returns:
            List of column headers.
        """
        return [
            "Pulls",
            "Raw Probability",
            "First 5★ Probability",
            "Cumulative Probability",
        ]

    def format_rows(
        self, stats_data: CalculationResult
    ) -> Generator[List[str], None, None]:
        """Format calculation results into CSV rows.

        Args:
            stats_data: Calculation results to format.

        Yields:
            Formatted rows of data.
        """
        for i in range(len(stats_data.raw_probabilities)):
            yield [
                str(i + 1),  # Pull number
                f"{stats_data.raw_probabilities[i]:.6f}",
                f"{stats_data.first_5star_prob[i]:.6f}",
                f"{stats_data.cumulative_prob[i]:.6f}",
            ]
