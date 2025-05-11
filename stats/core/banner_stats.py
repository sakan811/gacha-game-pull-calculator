"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games
(Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations
for different banner types.
"""

from typing import Dict, Tuple, Any, List
import os
from pathlib import Path

from core.banner import BannerConfig
from core.calculation_strategy import CalculationStrategy, CalculationError
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
        self.formatter = BannerRowFormatter(config)

    def calculate_probabilities(self) -> None:
        """Calculate probabilities for the banner configuration."""
        logger.info(
            f"Calculating probabilities for {self.config.game_name} - {self.config.banner_type} banner..."
        )
        calc_params = {
            "config": self.config,
            "pity_range": range(1, 91),  # Configurable if needed
        }
        self.results = self.calculator.calculate(calc_params)
        logger.info(
            f"Finished calculating probabilities for {self.config.game_name} - {self.config.banner_type}."
        )

    def get_banner_rows(self) -> Tuple[List[str], List[List[Any]]]:
        """Get formatted header and rows for CSV output.

        Returns:
            Tuple containing header list and formatted row data.
        """
        header, rows_generator = self.formatter.get_rows(self.results)
        return header, list(rows_generator)

    def calculate_and_save(self) -> None:
        """Calculate banner statistics and save to CSV.

        Raises:
            CalculationError: If calculation or saving fails.
        """
        try:
            # Calculate probabilities
            results = self.calculator.calculate({"config": self.config})

            # Format results
            header = self.formatter.get_header()
            rows = list(self.formatter.format_rows(results))

            # Ensure output directory exists
            output_dir = (
                Path("csv_output") / self.config.game_name.lower().replace(" ", "_")
            )
            os.makedirs(output_dir, exist_ok=True)

            # Save results
            filename = (
                output_dir
                / f"{self.config.banner_type.lower().replace(' ', '_')}.csv"
            )
            metadata = [
                f"Game: {self.config.game_name}",
                f"Banner: {self.config.banner_type}",
            ]

            self.output_handler.write(
                str(filename),
                header,
                rows,
                metadata_row=metadata,
            )

            logger.info(f"Successfully saved results to {filename}")

        except Exception as e:
            logger.error(f"Failed to calculate or save results: {str(e)}")
            raise CalculationError(f"Failed to process banner: {str(e)}")
