# Main execution logic
from core.logging import Logger
from core.banner_config import BANNER_CONFIGS
from core.banner_stats import BannerStats  # Updated import
from typing import Dict, Any

logger = Logger().get_logger()


class StatsRunner:
    """Orchestrates the probability calculations and output for all configured banners."""

    def __init__(self, banner_configs: Dict[str, Any]):
        """
        Initializes the StatsRunner.

        Args:
            banner_configs (dict): A dictionary of banner configurations where keys
                                   are expected to be in 'game_bannertype' format.
        """
        self.banner_configs = banner_configs
        self.logger = logger

    def process_all_banners(self):
        """Runs probability calculations and output for all configured banners."""
        self.logger.info("Starting banner statistics processing...")
        if not self.banner_configs:
            self.logger.warning(
                "No banner configurations provided. Skipping processing."
            )
            return

        for config_key in self.banner_configs:
            try:
                # Attempt to parse game and banner type from the config_key
                parts = config_key.split("_", 1)
                if len(parts) < 2 or not parts[0] or not parts[1]:
                    self.logger.warning(
                        f"Skipping invalid config key format: '{config_key}'. Expected 'game_bannertype'."
                    )
                    continue

                game_input_type = parts[0]
                banner_input_type = parts[1]

                self.logger.info(
                    f"Processing banner config: {config_key} (Game: {game_input_type}, Banner: {banner_input_type})"
                )

                banner_analyzer = BannerStats(
                    game_type=game_input_type, banner_type=banner_input_type
                )

                file_paths = banner_analyzer.save_statistics_csv()

                if file_paths:
                    self.logger.info(
                        f"Successfully saved stats for {banner_analyzer.game_type} {banner_analyzer.banner_type}:"
                    )
                    for metric, path in file_paths.items():
                        self.logger.info(f"  {metric}: {path}")
                else:
                    self.logger.info(
                        f"Stats processed for {banner_analyzer.game_type} {banner_analyzer.banner_type}, but no CSV files were reported as generated."
                    )

            except ValueError as ve:
                self.logger.error(
                    f"Configuration or validation error for {config_key}: {ve}"
                )
            except Exception as e:
                self.logger.error(
                    f"Unexpected error processing {config_key}: {e}", exc_info=True
                )
        self.logger.info("Banner statistics processing finished.")


def main():
    """Run probability calculations and output for all supported banners and games."""
    runner = StatsRunner(BANNER_CONFIGS)
    runner.process_all_banners()


if __name__ == "__main__":
    main()
