"""Banner statistics calculation runner module."""

from pathlib import Path

from core.common.logging import get_logger
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from output.row_formatter import format_results, get_headers
from core.config.banner_config import BANNER_CONFIGS
from core.common.errors import (
    BannerError,
)

logger = get_logger(__name__)


class StatsRunner:
    """Runs banner statistics calculations."""

    def __init__(self) -> None:
        self.output_handler = CSVOutputHandler()
        self.banner_configs = BANNER_CONFIGS

    def run(self) -> None:
        """Run banner statistics calculations."""
        try:
            self._process_banners()
        except BannerError as e:
            logger.error(f"Banner error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise

    def _process_banners(self) -> None:
        """Process all banner configurations."""
        for game_type, banners in BANNER_CONFIGS.items():
            output_path = Path("csv_output") / f"{game_type.lower()}_all_banners.csv"
            all_results = []

            for banner_type, config in banners.items():
                if not hasattr(config, "game_name") or not hasattr(
                    config, "banner_type"
                ):
                    logger.warning(
                        f"Invalid config for {game_type} {banner_type}, skipping."
                    )
                    continue
                try:
                    calculator = ProbabilityCalculator(config)
                    results = calculator.calculate_probabilities()
                    formatted_data = format_results(config, results)
                    all_results.extend(formatted_data)
                except BannerError as e:
                    logger.warning(f"Skipping {game_type} {banner_type} banner: {e}")
                    continue
                except Exception as e:
                    logger.error(
                        f"Unexpected error processing {game_type} {banner_type}: {e}",
                        exc_info=True,
                    )
                    continue

            if all_results:
                self.output_handler.write(str(output_path), get_headers(), all_results)


def main() -> None:
    """Main entry point for banner statistics calculation."""
    runner = StatsRunner()
    try:
        runner.run()
    except BannerError as e:
        logger.error(f"Failed to complete banner calculations: {e}")
        raise SystemExit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
