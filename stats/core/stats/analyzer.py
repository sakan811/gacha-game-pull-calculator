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
    """Analyzes and formats banner statistics.
    
    This class orchestrates the banner statistics calculation process by:
    1. Coordinating between calculation strategy and configuration
    2. Managing the formatting of results
    3. Handling file output operations
    """

    def calculate_and_save(self) -> None:
        """Calculate banner statistics and save the results.

        Raises:
            CalculationError: If calculation fails
            ValidationError: If saving results fails
        """
        params = {
            "base_rate": self.config.base_rate,
            "hard_pity": self.config.hard_pity,
            "soft_pity_start": self.config.soft_pity_start_after,
            "rate_increase": self.config.rate_increase
        }
        
        try:
            self.calculate_stats(params)
            output_path = Path("csv_output") / self.config.game_name.lower().replace(" ", "_")
            output_path.mkdir(parents=True, exist_ok=True)
            output_file = output_path / f"{self.config.game_name.lower().replace(' ', '_')}_all_banners.csv"
            self.write_results(output_file)
        except Exception as e:
            logger.error(f"Failed to calculate and save banner stats: {str(e)}")
            raise CalculationError(f"Failed to calculate and save banner stats: {str(e)}")

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
            output_handler: Handler for CSV file operations
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
        self.formatter = StatsFormatter(config)
        self._results: Optional[CalculationResult] = None

    def calculate_stats(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate banner statistics and store the results.

        Args:
            params: Calculation parameters

        Returns:
            Calculation results

        Raises:
            CalculationError: If calculation fails
        """
        try:
            result = self.calculator.calculate(params)
            result.validate()
            self._results = result
            return result
        except Exception as e:
            logger.error(f"Failed to calculate stats: {str(e)}")
            raise CalculationError(f"Stats calculation failed: {str(e)}")

    def format_results(self) -> List[List[str]]:
        """Format the most recent calculation results for output.

        Returns:
            Formatted results as list of string lists

        Raises:
            ValidationError: If no results are available
        """
        if not self._results:
            raise ValidationError("No results available to format")
        return self.formatter.format_results(self._results)
    
    def write_results(self, output_path: Path) -> None:
        """Write formatted results to a CSV file.

        Args:
            output_path: Path to the output CSV file

        Raises:
            ValidationError: If no results are available
            CalculationError: If writing results fails
        """
        try:
            header = ["Pulls", "Raw Probability", "First 5★ Probability", "Cumulative Probability"]
            formatted_results = self.format_results()
            metadata = [
                f"Game: {self.config.game_name}",
                f"Banner: {self.config.banner_type}",
                f"Base Rate: {self.config.base_rate}",
                f"Hard Pity: {self.config.hard_pity}",
            ]
            self.output_handler.write(str(output_path), header, formatted_results, metadata)
        except Exception as e:
            logger.error(f"Failed to write results: {str(e)}")
            raise CalculationError(f"Failed to write results: {str(e)}")
