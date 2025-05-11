"""Banner statistics calculation runner."""

from pathlib import Path


from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from output.row_formatter import format_results, get_headers
from core.config.banner_config import BANNER_CONFIGS
from core.common.logging import get_logger

logger = get_logger(__name__)


def run_banner_stats():
    """Calculate and save banner statistics."""
    logger.info("Starting banner statistics calculation.")
    output_handler = CSVOutputHandler()
    for game_type, banners in BANNER_CONFIGS.items():
        output_path = (
            Path("csv_output")
            / f"{game_type.lower().replace(' ', '_')}_all_banners.csv"
        )
        all_results = []
        logger.info(f"Processing game type: {game_type}")
        for banner_type, config in banners.items():
            logger.info(f"Calculating probabilities for banner: {banner_type}")
            calculator = ProbabilityCalculator(config)
            try:
                probabilities = calculator.calculate_probabilities()
                formatted_data = format_results(config, *probabilities)
                all_results.extend(formatted_data)
                logger.info(f"Finished calculations for banner: {banner_type}")
            except Exception as e:
                logger.error(
                    f"Error calculating probabilities for {banner_type}: {e}",
                    exc_info=True,
                )
        try:
            output_handler.write(str(output_path), get_headers(), all_results)
            logger.info(f"Results written to {output_path}")
        except Exception as e:
            logger.error(f"Failed to write CSV for {game_type}: {e}", exc_info=True)
    logger.info("Banner statistics calculation completed.")


if __name__ == "__main__":
    run_banner_stats()
