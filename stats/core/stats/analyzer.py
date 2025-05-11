"""Utility functions for analyzing banner statistics.

This module provides helper functions for analyzing banner statistics.
Main functionality has been moved to core.calculator.
"""

from typing import Dict, Any, List
from pathlib import Path

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
        Calculation results

    Raises:
        CalculationError: If analysis fails
    """
    calculator = ProbabilityCalculator(config)
    return calculator.calculate()


def get_banner_stats(configs: List[BannerConfig]) -> Dict[str, CalculationResult]:
    """Get statistics for multiple banner configurations.

    Args:
        configs: List of banner configurations to analyze

    Returns:
        Dictionary mapping banner names to calculation results
    """
    results = {}
    for config in configs:
        try:
            results[f"{config.game_name}_{config.banner_type}"] = analyze_banner(config)
        except CalculationError as e:
            logger.warning(f"Failed to analyze {config.game_name} {config.banner_type}: {e}")
            continue
    return results
