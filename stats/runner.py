from core.logging import Logger
from core.banner_config import BANNER_CONFIGS
from core.banner import BannerConfig
from core.banner_stats import BannerStats
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from typing import Dict, Any

logger = Logger().get_logger()


class StatsRunner:
    """Orchestrates the probability calculations and output for all configured banners."""

    def __init__(self, banner_configs: Dict[str, Any]):
        if not isinstance(banner_configs, dict):
            raise TypeError("banner_configs must be a dictionary.")
        self.banner_configs = banner_configs
        self.csv_handler = CSVOutputHandler()

    def process_all_banners(self):
        logger.info("Starting banner statistics processing...")
        game_rows = {}
        game_headers = {}
        for config_key, banner_config_data in self.banner_configs.items():
            game_name = getattr(banner_config_data, "game_name", "UnknownGame")
            banner_type = getattr(banner_config_data, "banner_type", "UnknownBanner")
            try:
                logger.info(
                    f"Processing banner: {config_key} ({game_name} - {banner_type})"
                )
                if not isinstance(banner_config_data, BannerConfig):
                    raise TypeError(
                        f"Configuration for '{config_key}' is not a valid BannerConfig object. Received type: {type(banner_config_data).__name__}"
                    )
                calculator = ProbabilityCalculator()
                banner_analyzer = BannerStats(
                    config=banner_config_data,
                    calculator=calculator,
                    output_handler=self.csv_handler,
                )
                banner_analyzer.calculate_probabilities()
                header, rows = banner_analyzer.get_banner_rows()
                game = banner_analyzer.game_name
                if game not in game_rows:
                    game_rows[game] = []
                    game_headers[game] = header
                game_rows[game].extend(rows)
                logger.info(
                    f"Prepared stats for {game} {banner_analyzer.banner_type} ({len(rows)} rows)"
                )
            except (ValueError, TypeError) as err:
                logger.error(
                    f"Error for {config_key} ({game_name} - {banner_type}): {err}",
                    exc_info=True,
                )
            except Exception as e:
                logger.error(
                    f"Unexpected error processing {config_key} ({game_name} - {banner_type}): {e}",
                    exc_info=True,
                )

        import os

        for game, rows in game_rows.items():
            safe_game = game.lower().replace(" ", "_")
            out_dir = os.path.join("csv_output", safe_game)
            os.makedirs(out_dir, exist_ok=True)
            filename = os.path.join(out_dir, f"{safe_game}_all_banners.csv")
            header = game_headers[game]
            try:
                self.csv_handler.write(filename, header, rows)
                logger.info(f"Successfully saved stats for {game}: {filename}")
            except Exception as e:
                logger.error(f"Failed to write CSV for {game}: {e}", exc_info=True)
        logger.info("Banner statistics processing finished.")


def main():
    try:
        runner = StatsRunner(BANNER_CONFIGS)
        runner.process_all_banners()
    except Exception as e:
        logger.critical(f"Failed to initialize or run StatsRunner: {e}", exc_info=True)


if __name__ == "__main__":
    main()
