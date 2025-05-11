"""Module for analyzing banner statistics."""
from typing import Dict, Any, List

from ..calculation.calculator import ProbabilityCalculator
from ..calculation.strategy import CalculationResult
from ..config.banner import BannerConfig
from ..common.errors import CalculationError
from ..common.logging import get_logger
from .formatter import StatsFormatter

logger = get_logger(__name__)


class BannerStats:
    """Analyzes banner statistics."""

    def __init__(self, config: BannerConfig, calculator: ProbabilityCalculator) -> None:
        self.config = config
        self.calculator = calculator
        self.formatter = StatsFormatter(config)

    def calculate_stats(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate banner statistics.
        
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
            return result
        except Exception as e:
            logger.error(f"Failed to calculate stats: {str(e)}")
            raise CalculationError(f"Stats calculation failed: {str(e)}")

    def format_results(self, results: CalculationResult) -> List[List[str]]:
        """Format calculation results for output.
        
        Args:
            results: Calculation results to format
            
        Returns:
            Formatted results as list of string lists
        """
        return self.formatter.format_results(results)
