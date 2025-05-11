"""Handles formatting of banner data into CSV rows."""

from typing import Dict, List, Any, Tuple, Generator
from core.banner import BannerConfig


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
            "Game",
            "Banner Type",
            "Pity",
            "Probability",
            "Cumulative Probability",
            "Expected Pulls",
        ]

    def format_rows(
        self, stats_data: Dict[str, Any]
    ) -> Generator[List[Any], None, None]:
        """Format statistical data into CSV rows.

        Args:
            stats_data: Dictionary containing statistical calculations.

        Yields:
            List containing formatted row data.
        """
        for pity, data in stats_data.items():
            yield [
                self.config.game_name,
                self.config.banner_type,
                pity,
                data.get("probability", 0),
                data.get("cumulative", 0),
                data.get("expected_pulls", 0),
            ]

    def get_rows(
        self, stats_data: Dict[str, Any]
    ) -> Tuple[List[str], Generator[List[Any], None, None]]:
        """Get both header and formatted rows.

        Args:
            stats_data: Dictionary containing statistical calculations.

        Returns:
            Tuple containing header list and generator of row data.
        """
        return self.get_header(), self.format_rows(stats_data)
