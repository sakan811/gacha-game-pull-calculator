"""Banner statistics calculation runner module."""
from typing import Dict, Any, List, Optional, Callable, TypeVar
from pathlib import Path
import time
from functools import wraps

from core.logging import Logger
from core.banner_config import BANNER_CONFIGS
from core.banner import BannerConfig
from core.banner_stats import BannerStats
from core.standard_calculation_strategy import StandardCalculationStrategy
from core.calculation_strategy import CalculationError
from output.csv_handler import CSVOutputHandler

logger = Logger().get_logger()

T = TypeVar('T')

def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying operations on failure.
    
    Args:
        max_retries: Maximum number of retry attempts.
        delay: Delay between retries in seconds.
        
    Returns:
        Decorated function that implements retry logic.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            if last_error is not None:
                raise last_error
            raise RuntimeError("Unexpected state in retry logic")
        return wrapper
    return decorator


class StatsRunner:
    """Orchestrates banner statistics calculations with error handling and progress tracking."""

    def __init__(self, banner_configs: Dict[str, Any]) -> None:
        self.banner_configs = banner_configs
        self.calculator = StandardCalculationStrategy()
        self.output_handler = CSVOutputHandler()
        self.total_configs = len(banner_configs)
        self.processed_configs = 0

    @retry_on_error()
    def process_banner(self, config: BannerConfig) -> None:
        """Process a single banner configuration with retry logic.
        
        Args:
            config: Banner configuration to process.
            
        Raises:
            CalculationError: If processing fails after all retries.
        """
        try:
            stats = BannerStats(config, self.calculator, self.output_handler)
            stats.calculate_and_save()
            self.processed_configs += 1
            logger.info(f"Progress: {self.processed_configs}/{self.total_configs} banners processed")
        except Exception as e:
            logger.error(f"Error processing banner {config.game_name}-{config.banner_type}: {str(e)}")
            raise CalculationError(f"Failed to process banner: {str(e)}")

    def process_all_banners(self) -> None:
        """Process all banner configurations with progress tracking."""
        logger.info(f"Starting processing of {self.total_configs} banner configurations")
        configs = self._process_banner_configs()
        
        for game_name, game_configs in configs.items():
            logger.info(f"Processing {game_name} banners")
            for config in game_configs.values():
                self.process_banner(config)
                
        logger.info("All banner configurations processed successfully")

    def _process_banner_configs(self) -> Dict[str, Dict[str, BannerConfig]]:
        """Process banner configurations with validation.
        
        Returns:
            Dictionary of processed and validated banner configurations.
            
        Raises:
            ValueError: If a configuration is invalid.
        """
        processed_configs: Dict[str, Dict[str, BannerConfig]] = {}
        for game_name, game_config in self.banner_configs.items():
            processed_configs[game_name] = {}
            for banner_type, config in game_config.items():
                try:
                    banner_config = BannerConfig(**config)
                    processed_configs[game_name][banner_type] = banner_config
                except (ValueError, TypeError) as e:
                    logger.error(f"Invalid configuration for {game_name}-{banner_type}: {str(e)}")
                    continue
        return processed_configs


def main() -> None:
    """Main entry point for banner statistics calculation."""
    try:
        runner = StatsRunner(BANNER_CONFIGS)
        runner.process_all_banners()
    except Exception as e:
        logger.critical(f"Failed to initialize or run StatsRunner: {e}", exc_info=True)


if __name__ == "__main__":
    main()
