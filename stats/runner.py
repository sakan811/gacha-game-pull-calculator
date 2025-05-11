"""Banner statistics calculation runner module."""

from typing import Mapping, cast
from pathlib import Path

from core.common.logging import get_logger
from core.config import BannerConfig
from core.stats.analyzer import BannerStats
from output.csv_handler import CSVOutputHandler
from core.calculation.standard_calculation_strategy import StandardCalculationStrategy
from core.config.banner_config import BANNER_CONFIGS

logger = get_logger(__name__)


class StatsRunner:
    """Orchestrates banner statistics calculations with error handling and progress tracking."""

    def __init__(
        self, banner_configs: Mapping[str, Mapping[str, BannerConfig]]
    ) -> None:
        self.banner_configs = banner_configs
        self.calculator = StandardCalculationStrategy()
        self.output_handler = CSVOutputHandler()
        self.processed_configs = 0

    def process_banner(self, config: BannerConfig) -> None:
        """Process a single banner configuration.

        Args:
            config: Banner configuration to process.

        Raises:
            CalculationError: If processing fails.
        """
        stats = BannerStats(config, self.calculator, self.output_handler)

        # Prepare calculation parameters from config
        params = {
            "base_rate": config.base_rate,
            "four_star_rate": config.four_star_rate,
            "soft_pity_start": config.soft_pity_start_after,
            "hard_pity": config.hard_pity,
            "rate_increase": config.rate_increase,
            "guaranteed_rate_up": config.guaranteed_rate_up,
            "rate_up_chance": config.rate_up_chance,
        }

        # Calculate probabilities
        stats.calculate(params)

        # Save results to CSV
        stats.write_results(Path("csv_output"))

        self.processed_configs += 1
        logger.info(f"Processed {config.game_name} - {config.banner_type} banner")

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
                    raise

        if self.processed_configs == total_configs:
            logger.info("All banner configurations processed successfully")


def main() -> None:
    """Main entry point for banner statistics calculation."""
    try:
        # Ensure output directory exists and is empty
        output_dir = Path("csv_output")
        if output_dir.exists():
            for file in output_dir.glob("*.csv"):
                file.unlink()
        else:
            output_dir.mkdir()

        # Run calculations
        runner = StatsRunner(
            cast(Mapping[str, Mapping[str, BannerConfig]], BANNER_CONFIGS)
        )
        runner.process_all_banners()
    except Exception as e:
        logger.critical(f"Failed to initialize or run StatsRunner: {e}")
        raise


if __name__ == "__main__":
    main()
