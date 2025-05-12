"""Banner statistics calculation runner with light OOP wrapper."""

from pathlib import Path
from typing import Optional, Dict, Any

from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from output.row_formatter import format_results, get_headers
from core.config.banner_config import BANNER_CONFIGS
from core.common.logging import get_logger


class BannerStatisticsRunner:
    """Runs banner statistics calculation with configurable dependencies."""

    def __init__(
        self,
        banner_configs: Optional[Dict[str, Dict[str, Any]]] = None,
        output_handler: Optional[CSVOutputHandler] = None,
        logger: Optional[Any] = None,
    ):
        """
        Initialize the runner with optional dependency injection.

        Args:
            banner_configs: Dictionary of banner configurations (defaults to BANNER_CONFIGS)
            output_handler: CSV output handler (defaults to CSVOutputHandler())
            logger: Logger instance (defaults to get_logger(__name__))
        """
        self.banner_configs = banner_configs or BANNER_CONFIGS
        self.output_handler = output_handler or CSVOutputHandler()
        self.logger = logger or get_logger(__name__)

    def _create_output_directory(self) -> None:
        """Ensure output directory exists."""
        Path("csv_output").mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """Calculate and save banner statistics."""
        self.logger.info("Starting banner statistics calculation.")
        self._create_output_directory()

        for game_type, banners in self.banner_configs.items():
            output_path = (
                Path("csv_output")
                / f"{game_type.lower().replace(' ', '_')}_all_banners.csv"
            )
            all_results = []

            self.logger.info(f"Processing game type: {game_type}")

            for banner_type, config in banners.items():
                self.logger.info(f"Calculating probabilities for banner: {banner_type}")

                try:
                    calculator = ProbabilityCalculator(config)
                    probabilities = calculator.calculate_probabilities()
                    formatted_data = format_results(config, *probabilities)
                    all_results.extend(formatted_data)

                    self.logger.info(f"Finished calculations for banner: {banner_type}")

                except Exception as e:
                    self.logger.error(
                        f"Error calculating probabilities for {banner_type}: {e}",
                        exc_info=True,
                    )

            try:
                self.output_handler.write(str(output_path), get_headers(), all_results)
                self.logger.info(f"Results written to {output_path}")

            except Exception as e:
                self.logger.error(
                    f"Failed to write CSV for {game_type}: {e}", exc_info=True
                )

        self.logger.info("Banner statistics calculation completed.")


def run_banner_stats() -> None:
    """
    Entry point for running banner statistics calculation.
    Maintains backwards compatibility with existing scripts.
    """
    runner = BannerStatisticsRunner()
    runner.run()


if __name__ == "__main__":
    run_banner_stats()
