"""Banner statistics calculation runner module."""

from typing import Dict, Any, Callable, TypeVar, Mapping, cast
import time
from functools import wraps

from core.common.errors import CalculationError
from core.common.logging import get_logger
from core.config import BannerConfig
from core.stats.analyzer import BannerStats
from output.csv_handler import CSVOutputHandler
from core.calculation.standard_calculation_strategy import StandardCalculationStrategy
from core.config.banner_config import BANNER_CONFIGS

logger = get_logger(__name__)

T = TypeVar("T")


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

    def __init__(self, banner_configs: Mapping[str, Mapping[str, BannerConfig]]) -> None:
        self.banner_configs = banner_configs
        self.calculator = StandardCalculationStrategy()
        self.output_handler = CSVOutputHandler()
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
            logger.info(
                f"Processed {config.game_name} - {config.banner_type} banner"
            )
        except Exception as e:
            logger.error(
                f"Error processing {config.game_name} - {config.banner_type} banner: {str(e)}"
            )
            raise CalculationError(f"Failed to process banner: {str(e)}")

    def process_all_banners(self) -> None:
        """Process all banner configurations with progress tracking."""
        total_configs = sum(
            len(game_banners) for game_banners in self.banner_configs.values()
        )
        logger.info(f"Starting processing of {total_configs} banner configurations")

        for game_name, game_banners in self.banner_configs.items():
            logger.info(f"Processing {game_name} banners")
            for banner_type, config in game_banners.items():
                try:
                    self.process_banner(config)
                except Exception as e:
                    logger.error(
                        f"Error processing {game_name} {banner_type} banner: {str(e)}"
                    )

        if self.processed_configs == total_configs:
            logger.info("All banner configurations processed successfully")
        else:
            logger.warning(
                f"Processed {self.processed_configs}/{total_configs} banner configurations"
            )


def main() -> None:
    """Main entry point for banner statistics calculation."""
    try:
        runner = StatsRunner(cast(Mapping[str, Mapping[str, BannerConfig]], BANNER_CONFIGS))
        runner.process_all_banners()
    except Exception as e:
        logger.critical(f"Failed to initialize or run StatsRunner: {e}")


if __name__ == "__main__":
    main()
