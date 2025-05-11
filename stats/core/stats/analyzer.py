"""Utility functions for analyzing banner statistics.

This module provides helper functions for analyzing banner statistics.
Main functionality has been moved to core.calculator.
"""

from typing import Dict, List

from core.config.banner import BannerConfig
from core.calculator import ProbabilityCalculator, CalculationResult
from core.common.errors import CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)


def analyze_banner(config: BannerConfig) -> CalculationResult:
    """Analyze a single banner configuration.

    Args:
        config: Banner configuration to analyze

    Returns:
        CalculationResult containing probability data

    Raises:
        CalculationError: If analysis fails
    """
    try:
        calculator = ProbabilityCalculator(config)
        return calculator.calculate_probabilities()
    except Exception as e:
        logger.error(
            f"Failed to analyze banner {config.banner_type}: {str(e)}", exc_info=True
        )
        raise CalculationError(f"Banner analysis failed: {str(e)}")


def get_banner_stats(configs: List[BannerConfig]) -> Dict[str, CalculationResult]:
    """Get statistics for multiple banner configurations.

    Args:
        configs: List of banner configurations to analyze

    Returns:
        Dictionary mapping banner types to calculation results

    Raises:
        CalculationError: If any analysis fails
    """
    results: Dict[str, CalculationResult] = {}

    for config in configs:
        try:
            results[config.banner_type] = analyze_banner(config)
        except Exception as e:
            logger.error(
                f"Failed to get stats for {config.banner_type}: {str(e)}", exc_info=True
            )
            raise CalculationError(f"Failed to get banner stats: {str(e)}")

    return results
