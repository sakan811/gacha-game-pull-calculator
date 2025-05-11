"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games
(Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations
for different banner types.
"""

from typing import Dict, Tuple, Any, List

from core.banner import BannerConfig
from core.calculation_strategy import CalculationStrategy
from output.csv_handler import CSVOutputHandler
from output.row_formatter import BannerRowFormatter
from core.logging import Logger

logger = Logger().get_logger()


class BannerStats:
    """Analyzes and formats banner statistics."""

    def __init__(
        self,
        config: BannerConfig,
        calculator: CalculationStrategy,
        output_handler: CSVOutputHandler,
    ) -> None:
        """Initialize BannerStats with configuration and dependencies.

        Args:
            config: Banner configuration details
            calculator: Strategy for probability calculations
            output_handler: Handler for CSV output
        """
        self.config = config
        self.calculator = calculator
        self.output_handler = output_handler
        self.game_name = config.game_name
        self.banner_type = config.banner_type
        self.formatter = BannerRowFormatter(config)
        self.results: Dict[str, Any] = {}

    def calculate_probabilities(self) -> None:
        """Calculate probabilities for the banner configuration."""
        logger.info(
            f"Calculating probabilities for {self.game_name} - {self.banner_type} banner..."
        )
        calc_params = {
            "config": self.config,
            "pity_range": range(1, 91),  # Configurable if needed
        }
        self.results = self.calculator.calculate(calc_params)
        logger.info(
            f"Finished calculating probabilities for {self.game_name} - {self.banner_type}."
        )

    def get_banner_rows(self) -> Tuple[List[str], List[List[Any]]]:
        """Get formatted header and rows for CSV output.

        Returns:
            Tuple containing header list and formatted row data.
        """
        header, rows_generator = self.formatter.get_rows(self.results)
        return header, list(rows_generator)
