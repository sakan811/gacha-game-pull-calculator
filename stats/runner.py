"""Banner statistics calculation runner module."""

from pathlib import Path
from core.common.logging import get_logger
from core.standard_calculation_strategy import StandardCalculationStrategy
from output.csv_handler import CSVOutputHandler
from core.config.banner_config import BANNER_CONFIGS

logger = get_logger(__name__)


class StatsRunner:
    """Runs banner statistics calculations."""

    def __init__(self) -> None:
        self.calculator = StandardCalculationStrategy()
        self.output_handler = CSVOutputHandler()

    def run(self) -> None:
        """Process all banner configurations and save results."""
        logger.info("Starting banner calculations")

        # Create or clear output directory
        output_dir = Path("csv_output")
        output_dir.mkdir(exist_ok=True)
        for file in output_dir.glob("*.csv"):
            file.unlink()

        # Process each game's banners
        for game_name, game_banners in BANNER_CONFIGS.items():
            for banner_type, config in game_banners.items():
                try:
                    # Calculate stats
                    params = {
                        "base_rate": config.base_rate,
                        "four_star_rate": config.four_star_rate,
                        "soft_pity_start": config.soft_pity_start_after,
                        "hard_pity": config.hard_pity,
                        "rate_increase": config.rate_increase,
                        "guaranteed_rate_up": config.guaranteed_rate_up,
                        "rate_up_chance": config.rate_up_chance,
                    }
                    results = self.calculator.calculate(params)

                    # Save results
                    filename = f"{game_name.lower().replace(' ', '_')}_all_banners.csv"
                    self.output_handler.write(
                        str(output_dir / filename),
                        ["Game", "Banner Type", "Roll", "Probability", "Cumulative"],
                        self._format_results(config, results),
                    )
                    logger.info(f"Processed {game_name} {banner_type} banner")
                except Exception as e:
                    logger.error(f"Error processing {game_name} {banner_type}: {e}")
                    raise

        logger.info("All banner configurations processed successfully")

    def _format_results(self, config, results):
        """Format results for CSV output."""
        rows = []
        for i, (prob, cum_prob) in enumerate(
            zip(results.raw_probabilities, results.cumulative_prob), 1
        ):
            rows.append(
                [
                    config.game_name,
                    config.banner_type,
                    str(i),
                    f"{prob:.6f}",
                    f"{cum_prob:.6f}",
                ]
            )
        return rows


def main() -> None:
    """Main entry point for banner statistics calculation."""
    try:
        runner = StatsRunner()
        runner.run()
    except Exception as e:
        logger.critical(f"Failed to run banner calculations: {e}")
        raise


if __name__ == "__main__":
    main()
