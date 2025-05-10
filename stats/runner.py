# Main execution logic
from core.logging import Logger
from core.banner_config import BANNER_CONFIGS
from core.banner import BannerConfig  # Added import
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
            # Safely get game_name and banner_type for logging, even if banner_config_data is not a proper object
            game_name_for_log = getattr(banner_config_data, "game_name", "UnknownGame")
            banner_type_for_log = getattr(banner_config_data, "banner_type", "UnknownBanner")
            try:
                logger.info(
                    f"Processing banner: {config_key} ({game_name_for_log} - {banner_type_for_log})"
                )

                if not isinstance(banner_config_data, BannerConfig):
                    raise TypeError(
                        f"Configuration for '{config_key}' is not a valid BannerConfig object. "
                        f"Received type: {type(banner_config_data).__name__}"
                    )

                # If we've passed the isinstance check, banner_config_data is a BannerConfig object,
                # so direct access is safe from here on within this try block.
                calculator = (
                    ProbabilityCalculator()
                )

                banner_analyzer = BannerStats(
                    config=banner_config_data,
                    calculator=calculator,
                    output_handler=self.csv_handler,
                )

                banner_analyzer.calculate_probabilities()
                file_paths = banner_analyzer.save_results_to_csv()

                if file_paths:
                    logger.info(
                        f"Successfully saved stats for {banner_analyzer.config.game_name} {banner_analyzer.config.banner_type}:"
                    )
                    for metric, path in file_paths.items():
                        logger.info(f"  {metric}: {path}")
                else:
                    logger.info(
                        f"Stats processed for {banner_analyzer.config.game_name} {banner_analyzer.config.banner_type}, but no CSV files were reported as generated."
                    )

            except ValueError as ve:  # Handles issues from ProbabilityCalculator or BannerStats based on valid config values
                logger.error(
                    f"Configuration or validation error for {config_key} ({game_name_for_log} - {banner_type_for_log}): {ve}"
                )
            except TypeError as te:  # Catches the TypeError from isinstance check or other type issues
                logger.error(
                    f"Type error or invalid config structure for {config_key} ({game_name_for_log} - {banner_type_for_log}): {te}",
                    exc_info=True,
                )
            except Exception as e:  # Catch-all for other unexpected errors
                logger.error(
                    f"Unexpected error processing {config_key} ({game_name_for_log} - {banner_type_for_log}): {e}",
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
