"""Banner statistics calculation runner."""
from pathlib import Path

from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from output.row_formatter import format_results, get_headers
from core.config.banner_config import BANNER_CONFIGS


def run_banner_stats():
    """Calculate and save banner statistics."""
    output_handler = CSVOutputHandler()
    for game_type, banners in BANNER_CONFIGS.items():
        output_path = Path("csv_output") / f"{game_type.lower()}_all_banners.csv"
        all_results = []
        for banner_type, config in banners.items():
            calculator = ProbabilityCalculator(config)
            probabilities = calculator.calculate_probabilities()
            formatted_data = format_results(config, *probabilities)
            all_results.extend(formatted_data)
        output_handler.write(str(output_path), get_headers(), all_results)


if __name__ == "__main__":
    run_banner_stats()
