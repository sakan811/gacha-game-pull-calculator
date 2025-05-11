"""Handles formatting of calculation results for output.

This module provides functionality to format banner calculation results into a
standardized format suitable for CSV output.
"""

from typing import List, Final
from decimal import Decimal, ROUND_HALF_UP

from ..core.config.banner_config import BannerConfig
from ..core.common.logging import get_logger

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


def format_results(
    config: BannerConfig,
    per_roll: list[float],
    cumulative: list[float],
    first_5star: list[float],
) -> List[List[str]]:
    """Format probability lists into CSV rows."""
    return [
        [
            config.game_name,
            config.banner_type,
            str(i),
            format_number(prob),
            format_number(cum),
            format_number(first),
        ]
        for i, (prob, cum, first) in enumerate(
            zip(per_roll, cumulative, first_5star), 1
        )
    ]


def get_headers() -> List[str]:
    """Get the column headers for output.

    Returns:
        List of column header strings
    """
    return COLUMN_HEADERS.copy()
