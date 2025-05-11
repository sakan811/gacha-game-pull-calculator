"""Handles formatting of banner data into CSV rows.

This module provides functionality to format banner calculation results into CSV-compatible
rows with proper formatting and validation of data.
"""

from typing import List, Generator, Optional, Final
import numpy as np

from core.banner import BannerConfig
from core.calculation_strategy import CalculationResult
from core.common.errors import ValidationError
from core.common.logging import get_logger

logger = get_logger(__name__)

# Constants for formatting
DECIMAL_PLACES: Final[int] = 6
COLUMN_HEADERS: Final[List[str]] = [
    "Game",
    "Banner Type", 
    "Roll Number",
    "Probability per Roll",
    "Cumulative Probability",
    "First 5 Star Probability"
]


class BannerRowFormatter:
    """Formats banner data into CSV rows.

    This class handles the conversion of numerical calculation results
    into properly formatted strings for CSV output, including validation
    and proper number formatting.

    Attributes:
        config: Banner configuration for context
        last_result: Last formatted result for caching
    """

    def __init__(self, config: BannerConfig) -> None:
        """Initialize formatter with banner configuration.

        Args:
            config: Banner configuration parameters

        Raises:
            ValidationError: If config is invalid
        """
        if not isinstance(config, BannerConfig):
            raise ValidationError("Invalid banner configuration provided")

        self.config = config
        self.last_result: Optional[CalculationResult] = None

    def get_header(self) -> List[str]:
        """Generate the CSV header row.

        Returns:
            List of column headers
        """
        return COLUMN_HEADERS.copy()

    def validate_calculation_result(self, result: CalculationResult) -> None:
        """Validate calculation result data before formatting.

        Args:
            result: Calculation results to validate

        Raises:
            ValidationError: If result data is invalid
        """
        if not isinstance(result, CalculationResult):
            raise ValidationError("Invalid calculation result type")

        expected_length = self.config.hard_pity

        # Validate array lengths
        if len(result.raw_probabilities) != expected_length:
            raise ValidationError(
                f"Raw probabilities length {len(result.raw_probabilities)} "
                f"does not match hard pity {expected_length}"
            )

        if len(result.first_5star_prob) != expected_length:
            raise ValidationError(
                f"First 5★ probabilities length {len(result.first_5star_prob)} "
                f"does not match hard pity {expected_length}"
            )

        if len(result.cumulative_prob) != expected_length:
            raise ValidationError(
                f"Cumulative probabilities length {len(result.cumulative_prob)} "
                f"does not match hard pity {expected_length}"
            )

        # Validate probability bounds
        arrays_to_check = [
            ("Raw probabilities", result.raw_probabilities),
            ("First 5★ probabilities", result.first_5star_prob),
            ("Cumulative probabilities", result.cumulative_prob),
        ]

        for name, array in arrays_to_check:
            if not np.all((array >= 0) & (array <= 1)):
                raise ValidationError(f"{name} contains invalid probability values")

    def format_probability(self, value: float) -> str:
        """Format a probability value as a string.

        Args:
            value: Probability value to format

        Returns:
            Formatted string with fixed decimal places
        """
        return f"{value:.{DECIMAL_PLACES}f}"

    def format_rows(
        self, stats_data: CalculationResult
    ) -> Generator[List[str], None, None]:
        """Format calculation results into CSV rows.

        Args:
            stats_data: Calculation results to format

        Yields:
            Formatted rows of data matching required CSV structure:
            Game,Banner Type,Roll Number,Probability per Roll,Cumulative Probability,First 5 Star Probability

        Raises:
            ValidationError: If data validation fails
        """
        try:
            self.validate_calculation_result(stats_data)
            self.last_result = stats_data

            for i in range(len(stats_data.raw_probabilities)):
                yield [
                    self.config.game_name,  # Game name
                    self.config.banner_type,  # Banner type  
                    str(i + 1),  # Roll number
                    self.format_probability(stats_data.raw_probabilities[i]),  # Probability per roll
                    self.format_probability(stats_data.cumulative_prob[i]),  # Cumulative probability
                    self.format_probability(stats_data.first_5star_prob[i]),  # First 5* probability
                ]

        except Exception as e:
            logger.error(f"Failed to format rows: {str(e)}")
            raise ValidationError(f"Failed to format calculation results: {str(e)}")

    def get_summary_rows(self) -> List[List[str]]:
        """Generate summary statistics rows.

        Returns:
            List of summary rows with key statistics

        Raises:
            ValidationError: If no results available
        """
        if not self.last_result:
            raise ValidationError("No calculation results available for summary")

        try:
            result = self.last_result

            return [
                ["Summary Statistics"],
                ["Average 5★ pulls", self.format_probability(np.average(
                    np.arange(1, len(result.raw_probabilities) + 1),
                    weights=result.first_5star_prob
                ))],
                ["50% chance at pull", str(np.searchsorted(
                    result.cumulative_prob, 0.5
                ) + 1)],
                ["90% chance at pull", str(np.searchsorted(
                    result.cumulative_prob, 0.9
                ) + 1)],
                ["99% chance at pull", str(np.searchsorted(
                    result.cumulative_prob, 0.99
                ) + 1)],
            ]

        except Exception as e:
            logger.error(f"Failed to generate summary: {str(e)}")
            raise ValidationError(f"Failed to generate summary statistics: {str(e)}")
