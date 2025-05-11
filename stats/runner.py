"""Banner statistics calculation runner module."""

from pathlib import Path

from core.common.logging import get_logger
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from output.row_formatter import format_results, get_headers
from core.config.banner_config import BANNER_CONFIGS

logger = get_logger(__name__)


def run_banner_stats():
    output_handler = CSVOutputHandler()
    for game_type, banners in BANNER_CONFIGS.items():
        output_path = Path("csv_output") / f"{game_type.lower()}_all_banners.csv"
        all_results = []
        for banner_type, config in banners.items():
            try:
                calculator = ProbabilityCalculator(config)
                probs, first_5star, cumulative = calculator.calculate_probabilities()
                formatted_data = format_results(config, probs, first_5star, cumulative)
                all_results.extend(formatted_data)
            except Exception as e:
                logger.error(f"Error processing {game_type} {banner_type}: {e}")
        if all_results:
            output_handler.write(str(output_path), get_headers(), all_results)


def main():
    try:
        run_banner_stats()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
