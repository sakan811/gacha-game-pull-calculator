# Main execution logic stub
import logging

from core.banner_config import BANNER_CONFIGS
from core.banner_stats import BannerStats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(module)s - %(levelname)s - %(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler() # Outputs to console
    ]
)
logger = logging.getLogger(__name__)


class StatsRunner:
    """Orchestrates the probability calculations and output for banners."""

    def __init__(self, banner_configs):
        """
        Initializes the StatsRunner.

        Args:
            banner_configs (dict): A dictionary of banner configurations.
        """
        self.banner_configs = banner_configs

    def process_all_banners(self):
        """Runs probability calculations and output for all configured banners."""
        logger.info("Starting banner statistics processing...")
        for config_key in self.banner_configs:
            # Parse game and banner type from config key
            if "_" not in config_key:
                logger.warning(f"Skipping invalid config key format: {config_key}")
                continue
            
            game_type, banner_type = config_key.split("_", 1)
            
            try:
                logger.info(f"Processing banner: {game_type}_{banner_type}")
                stats = BannerStats(game_type=game_type, banner_type=banner_type)
                file_paths = stats.save_statistics_csv()
                logger.info(f"Successfully saved stats for {game_type} {banner_type}:")
                for metric, path in file_paths.items():
                    logger.info(f"{metric}: {path}")
            except Exception as e:
                logger.error(f"Error processing {config_key}: {e}", exc_info=True)
        logger.info("Banner statistics processing finished.")


def main():
    """Run probability calculations and output for all supported banners and games."""
    runner = StatsRunner(BANNER_CONFIGS)
    runner.process_all_banners()


if __name__ == "__main__":
    main()
