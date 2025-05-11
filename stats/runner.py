"""Banner statistics calculation runner module."""

import os
from typing import Dict, Any, Tuple, List, Optional

from core.logging import Logger
from core.banner_config import BANNER_CONFIGS
from core.banner import BannerConfig
from core.banner_stats import BannerStats
from core.standard_calculation_strategy import StandardCalculationStrategy
from output.csv_handler import CSVOutputHandler

logger = Logger().get_logger()


class StatsRunner:
    """Orchestrates the probability calculations and output for all configured banners."""

    def __init__(self, banner_configs: Dict[str, Any]) -> None:
        """Initialize StatsRunner with banner configurations.

        Args:
            banner_configs: Dictionary of banner configurations
        """
        if not isinstance(banner_configs, dict):
            raise TypeError("banner_configs must be a dictionary")
        self.banner_configs = banner_configs
        self.csv_handler = CSVOutputHandler()

    def process_all_banners(self) -> None:
        """Process all banner configurations and generate statistics."""
        logger.info("Starting banner statistics processing...")
        game_data = self._process_banner_configs()
        self._write_game_statistics(game_data)
        logger.info("Banner statistics processing finished.")

    def _process_banner_configs(self) -> Dict[str, Dict[str, Any]]:
        """Process each banner configuration and collect game-specific data.

        Returns:
            Dict containing game-specific rows and headers.
        """
        game_data: Dict[str, Dict[str, Any]] = {}

        for config_key, banner_config_data in self.banner_configs.items():
            game_name = getattr(banner_config_data, "game_name", "UnknownGame")
            banner_type = getattr(banner_config_data, "banner_type", "UnknownBanner")

            try:
                banner_result = self._process_single_banner(
                    config_key, game_name, banner_type, banner_config_data
                )
                if banner_result:
                    header, rows, game = banner_result
                    if game not in game_data:
                        game_data[game] = {"rows": [], "headers": header}
                    game_data[game]["rows"].extend(rows)
                    logger.info(f"Prepared stats for {game} {banner_type} ({len(rows)} rows)")

            except Exception as e:
                logger.error(
                    f"Unexpected error processing {config_key} ({game_name} - {banner_type}): {e}",
                    exc_info=True,
                )

        return game_data

    def _process_single_banner(
        self, config_key: str, game_name: str, banner_type: str, banner_config_data: Any
    ) -> Optional[Tuple[List[str], List[Any], str]]:
        """Process a single banner configuration.

        Args:
            config_key: Key identifying the banner configuration
            game_name: Name of the game
            banner_type: Type of banner
            banner_config_data: Banner configuration data

        Returns:
            Tuple of (header, rows, game_name) if successful, None if failed.

        Raises:
            TypeError: If banner_config_data is not a valid BannerConfig object
        """
        logger.info(f"Processing banner: {config_key} ({game_name} - {banner_type})")

        if not isinstance(banner_config_data, BannerConfig):
            raise TypeError(
                f"Configuration for '{config_key}' is not a valid BannerConfig object. "
                f"Received type: {type(banner_config_data).__name__}"
            )

        calculation_strategy = StandardCalculationStrategy()
        banner_analyzer = BannerStats(
            config=banner_config_data,
            calculator=calculation_strategy,
            output_handler=self.csv_handler,
        )

        banner_analyzer.calculate_probabilities()
        header, rows = banner_analyzer.get_banner_rows()
        rows = list(rows)  # Convert generator to list for length and multiple iterations

        return header, rows, banner_analyzer.game_name

    def _write_game_statistics(self, game_data: Dict[str, Dict[str, Any]]) -> None:
        """Write processed statistics to CSV files for each game.

        Args:
            game_data: Dictionary containing game-specific statistics
        """
        for game, data in game_data.items():
            safe_game = game.lower().replace(" ", "_")
            out_dir = os.path.join("csv_output", safe_game)
            os.makedirs(out_dir, exist_ok=True)

            filename = os.path.join(out_dir, f"{safe_game}_all_banners.csv")
            try:
                self.csv_handler.write(filename, data["headers"], data["rows"])
                logger.info(f"Successfully saved stats for {game}: {filename}")
            except Exception as e:
                logger.error(f"Failed to write CSV for {game}: {e}", exc_info=True)


def main() -> None:
    """Main entry point for banner statistics calculation."""
    try:
        runner = StatsRunner(BANNER_CONFIGS)
        runner.process_all_banners()
    except Exception as e:
        logger.critical(f"Failed to initialize or run StatsRunner: {e}", exc_info=True)


if __name__ == "__main__":
    main()
