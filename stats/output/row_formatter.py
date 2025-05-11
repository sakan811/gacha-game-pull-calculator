"""Handles formatting of calculation results for output.

This module provides functionality to format banner calculation results into a
standardized format suitable for CSV output.
"""

from typing import List, Final
from decimal import Decimal, ROUND_HALF_UP

from core.config.banner import BannerConfig
from core.calculator import CalculationResult
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
    "First 5 Star Probability",
]


def format_number(value: float, decimal_places: int = DECIMAL_PLACES) -> str:
    """Format a number with specified decimal places.

    Args:
        value: Number to format
        decimal_places: Number of decimal places to round to

    Returns:
        Formatted number string
    """
    # Use Decimal for precise rounding
    return str(
        Decimal(str(value)).quantize(
            Decimal("0." + "0" * decimal_places), rounding=ROUND_HALF_UP
        )
    )


def format_results(config: BannerConfig, results: CalculationResult) -> List[List[str]]:
    """Format calculation results for output.

    Args:
        config: Banner configuration
        results: Calculation results

    Returns:
        List of formatted rows
    """
    formatted_rows = []

    for i, (prob, cum, first) in enumerate(
        zip(
            results.raw_probabilities, results.cumulative_prob, results.first_5star_prob
        ),
        1,
    ):
        formatted_rows.append(
            [
                config.game_name,
                config.banner_type,
                str(i),
                format_number(prob),
                format_number(cum),
                format_number(first),
            ]
        )

    return formatted_rows


def get_headers() -> List[str]:
    """Get the column headers for output.

    Returns:
        List of column header strings
    """
    return COLUMN_HEADERS.copy()
