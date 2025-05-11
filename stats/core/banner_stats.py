"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games
(Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations
for different banner types and manages the calculation, formatting, and storage of results.
"""

from typing import Tuple, Any, List, Dict, Optional
from pathlib import Path
import os

from core.banner import BannerConfig
from core.calculation_strategy import (
    CalculationStrategy,
    CalculationResult,
    CalculationError,
)
from core.common.errors import ValidationError
from output.csv_handler import CSVOutputHandler, CSVValidationError
from output.row_formatter import BannerRowFormatter
from core.common.logging import get_logger

logger = get_logger(__name__)


class BannerStats:
    """Analyzes and formats banner statistics.

    This class orchestrates the banner statistics calculation process by:
    1. Coordinating between calculation strategy and configuration
    2. Managing the formatting of results
    3. Handling file output operations

    Attributes:
        config: Banner configuration parameters
        calculator: Strategy implementation for probability calculations
        output_handler: Handler for CSV file operations
        formatter: Formatter for converting results to CSV format
        results: Latest calculation results
    """

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

        Raises:
            ValidationError: If any component is invalid
        """
        if not isinstance(config, BannerConfig):
            raise ValidationError("Invalid banner configuration provided")
        if not isinstance(calculator, CalculationStrategy):
            raise ValidationError("Invalid calculation strategy provided")
        if not isinstance(output_handler, CSVOutputHandler):
            raise ValidationError("Invalid output handler provided")

        self.config = config
        self.calculator = calculator
        self.output_handler = output_handler
        self.formatter = BannerRowFormatter(config)
        self.results: Optional[CalculationResult] = None

    def calculate_probabilities(self) -> CalculationResult:
        """Calculate probabilities for the banner configuration.

        Performs probability calculations using the configured calculation strategy.

        Returns:
            CalculationResult containing the computed probabilities

        Raises:
            CalculationError: If calculation fails
        """
        logger.info(
            f"Calculating probabilities for {self.config.game_name} - {self.config.banner_type} banner..."
        )

        try:
            calc_params: Dict[str, Any] = {
                "config": self.config,
                "pity_range": range(1, self.config.hard_pity + 1),
            }

            self.results = self.calculator.calculate(calc_params)

            logger.info(
                f"Successfully calculated probabilities for {self.config.game_name} - "
                f"{self.config.banner_type} banner"
            )

            return self.results

        except Exception as e:
            logger.error(f"Probability calculation failed: {str(e)}")
            raise CalculationError(f"Failed to calculate probabilities: {str(e)}")

    def get_banner_rows(self) -> Tuple[List[str], List[List[Any]]]:
        """Get formatted header and rows for CSV output.

        Returns:
            Tuple containing:
                - List of column headers
                - List of data rows

        Raises:
            ValidationError: If results are not available
        """
        if not self.results:
            logger.error("Cannot format rows: No calculation results available")
            raise ValidationError("Must calculate probabilities before getting rows")

        try:
            header = self.formatter.get_header()
            rows = list(self.formatter.format_rows(self.results))
            return header, rows
        except Exception as e:
            logger.error(f"Failed to format banner rows: {str(e)}")
            raise ValidationError(f"Failed to format results: {str(e)}")

    def calculate_and_save(self) -> Path:
        """Calculate banner statistics and save to CSV.

        This method:
        1. Calculates probabilities using the strategy
        2. Formats results into CSV rows
        3. Creates output directory if needed
        4. Saves results to CSV file

        Returns:
            Path to the saved CSV file

        Raises:
            CalculationError: If calculation fails
            CSVValidationError: If CSV operations fail
            OSError: If file operations fail
        """
        try:
            # Calculate probabilities if not already done
            if not self.results:
                self.results = self.calculate_probabilities()

            # Format results
            header = self.formatter.get_header()
            rows = list(self.formatter.format_rows(self.results))

            # Prepare output path
            game_dir = self.config.game_name.lower().replace(" ", "_")
            banner_file = f"{self.config.banner_type.lower().replace(' ', '_')}.csv"
            output_dir = Path("csv_output") / game_dir

            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Prepare file path and metadata
            output_path = output_dir / banner_file
            metadata = [
                f"Game: {self.config.game_name}",
                f"Banner: {self.config.banner_type}",
                f"Base Rate: {self.config.base_rate}",
                f"Hard Pity: {self.config.hard_pity}",
            ]

            # Save results
            self.output_handler.write(
                str(output_path),
                header,
                rows,
                metadata_row=metadata,
            )

            logger.info(f"Successfully saved results to {output_path}")
            return output_path

        except CalculationError as e:
            logger.error(f"Calculation failed: {str(e)}")
            raise
        except CSVValidationError as e:
            logger.error(f"CSV validation failed: {str(e)}")
            raise
        except OSError as e:
            logger.error(f"File operation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise CalculationError(f"Failed to process banner: {str(e)}")
