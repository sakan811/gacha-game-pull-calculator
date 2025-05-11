"""Module for analyzing banner statistics."""

from typing import Dict, Any, List, Optional
from pathlib import Path

from core.calculation.strategy import CalculationStrategy, CalculationResult
from core.config.banner import BannerConfig
from core.common.errors import CalculationError, ValidationError
from core.common.logging import get_logger
from output.csv_handler import CSVOutputHandler
from .formatter import StatsFormatter

logger = get_logger(__name__)


class BannerStats:
    """Class for analyzing banner statistics."""

    def __init__(
        self,
        config: BannerConfig,
        strategy: Optional[CalculationStrategy] = None,
        output_handler: Optional[CSVOutputHandler] = None,
        formatter: Optional[StatsFormatter] = None,
    ) -> None:
        """Initialize the banner stats analyzer.

        Args:
            config: Banner configuration
            strategy: Optional calculation strategy
            output_handler: Optional CSV output handler
            formatter: Optional results formatter
        """
        self.config = config
        self.strategy = strategy
        self.output_handler = output_handler or CSVOutputHandler()
        self.formatter = formatter or StatsFormatter(config)
        self.results: Optional[CalculationResult] = None

    def calculate(self, params: Dict[str, Any]) -> None:
        """Calculate banner statistics.

        Args:
            params: Calculation parameters

        Raises:
            CalculationError: If no strategy is set or calculation fails
        """
        if not self.strategy:
            raise CalculationError("No calculation strategy set")

        try:
            self.results = self.strategy.calculate(params)
        except Exception as e:
            logger.error(f"Failed to calculate stats: {str(e)}")
            raise CalculationError(f"Failed to calculate stats: {str(e)}")

    def format_results(self) -> List[List[str]]:
        """Format the calculation results.

        Returns:
            Formatted results as a list of rows

        Raises:
            ValidationError: If no results are available
        """
        if not self.results:
            raise ValidationError("No results available to format")

        return self.formatter.format_rows(self.results)

    def write_results(self, output_path: Path) -> None:
        """Write formatted results to the game's CSV file.

        Args:
            output_path: Base path for the output CSV file

        Raises:
            ValidationError: If no results are available
            CalculationError: If writing results fails
        """
        if not self.results:
            raise ValidationError("No results available to write")

        try:
            # Create game-specific output file name
            game_name = self.config.game_name.lower().replace(" ", "_")
            output_file = output_path / f"{game_name}_all_banners.csv"

            # Get header and formatted results
            header = self.formatter.get_header()
            formatted_results = self.format_results()

            # Write or append results based on file existence
            self.output_handler.write(str(output_file), header, formatted_results)
            logger.info(
                f"Successfully wrote results for {self.config.banner_type} banner to {output_file}"
            )

        except Exception as e:
            logger.error(f"Failed to write results: {str(e)}")
            raise CalculationError(f"Failed to write results: {str(e)}")
