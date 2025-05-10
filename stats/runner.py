# Main execution logic
from core.logging import Logger
from core.banner_config import BANNER_CONFIGS
from core.banner_stats import BannerStats
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from typing import Dict, Any

logger = Logger().get_logger()


class StatsRunner:
    """Orchestrates the probability calculations and output for all configured banners."""

    def __init__(self, banner_configs: Dict[str, Any]):
        """
        Initializes the StatsRunner.

        Args:
            banner_configs (Dict[str, Any]): A dictionary of banner configurations.
        """
        if not isinstance(banner_configs, dict):
            raise TypeError("banner_configs must be a dictionary.")
        self.banner_configs = banner_configs
        self.csv_handler = CSVOutputHandler()

    def process_all_banners(self):
        """Processes each configured banner to calculate and save its statistics."""
        logger.info("Starting banner statistics processing...")
        for config_key, banner_config_data in self.banner_configs.items():
            logger.info(
                f"Processing banner: {config_key} ({banner_config_data.game_name} - {banner_config_data.banner_type})"
            )
            try:
                calculator = ProbabilityCalculator()  # Or a more specific one based on banner_config_data

                banner_analyzer = BannerStats(
                    config=banner_config_data,
                    calculator=calculator,
                    output_handler=self.csv_handler,
                )

                banner_analyzer.calculate_probabilities()
                file_paths = banner_analyzer.save_results_to_csv()

                if file_paths:
                    logger.info(
                        f"Successfully saved stats for {banner_analyzer.game_name} {banner_analyzer.banner_type}:"
                    )
                    for metric, path in file_paths.items():
                        logger.info(f"  {metric}: {path}")
                else:
                    logger.info(
                        f"Stats processed for {banner_analyzer.game_name} {banner_analyzer.banner_type}, but no CSV files were reported as generated."
                    )

            except ValueError as ve:
                logger.error(
                    f"Configuration or validation error for {config_key} ({banner_config_data.game_name} - {banner_config_data.banner_type}): {ve}"
                )
            except TypeError as te:
                logger.error(
                    f"Type error during setup for {config_key} ({banner_config_data.game_name} - {banner_config_data.banner_type}): {te}",
                    exc_info=True,
                )
            except Exception as e:
                logger.error(
                    f"Unexpected error processing {config_key} ({banner_config_data.game_name} - {banner_config_data.banner_type}): {e}",
                    exc_info=True,
                )
        logger.info("Banner statistics processing finished.")


def main():
    """Run probability calculations and output for all supported banners and games."""
    try:
        runner = StatsRunner(BANNER_CONFIGS)
        runner.process_all_banners()
    except Exception as e:
        logger.critical(f"Failed to initialize or run StatsRunner: {e}", exc_info=True)


if __name__ == "__main__":
    main()
