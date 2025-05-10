"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games (Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations for different banner types.
"""

# numpy is used by calculator, not directly here
from typing import Dict, Tuple, Any

from core.banner import BannerConfig
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from core.logging import Logger

logger = Logger().get_logger()


class BannerStats:
    """Calculates and prepares statistics for a single gacha banner."""

    def __init__(
        self,
        config: BannerConfig,
        calculator: ProbabilityCalculator,
        output_handler: CSVOutputHandler,
    ):
        """
        Initializes BannerStats with banner configuration, a probability calculator, and an output handler.

        Args:
            config (BannerConfig): The configuration for the banner.
            calculator (ProbabilityCalculator): The calculator instance for probability computations.
            output_handler (CSVOutputHandler): The handler for outputting results.
        """
        if not isinstance(config, BannerConfig):
            raise TypeError("config must be an instance of BannerConfig")
        if not isinstance(calculator, ProbabilityCalculator):
            raise TypeError("calculator must be an instance of ProbabilityCalculator")
        if not isinstance(output_handler, CSVOutputHandler):
            raise TypeError("output_handler must be an instance of CSVOutputHandler")

        self.config: BannerConfig = config
        self.calculator: ProbabilityCalculator = calculator
        self.output_handler: CSVOutputHandler = output_handler
        self.game_name: str = config.game_name
        self.banner_type: str = config.banner_type
        self.results: Dict[str, Any] = {}

    def calculate_probabilities(self) -> None:
        """Performs all probability calculations for the banner."""
        logger.info(
            f"Calculating probabilities for {self.game_name} - {self.banner_type} banner..."
        )
        self.calculator.config = self.config
        self.calculator._initialize_calculations()  # Call protected method, consider refactoring calculator if this is awkward

        raw_probs = self.calculator._calculate_raw_probabilities()
        first_5_star_probs = self.calculator._calculate_first_5star_prob_from_raw(
            raw_probs
        )
        cumulative_probs = self.calculator._calculate_cumulative_prob_from_raw(
            raw_probs
        )

        self.results = {
            "rolls": self.calculator.rolls,
            "raw_probabilities": raw_probs,
            "first_5_star_probabilities": first_5_star_probs,
            "cumulative_probabilities": cumulative_probs,
        }
        logger.info(
            f"Finished calculating probabilities for {self.game_name} - {self.banner_type}."
        )

    def _prepare_output_data(
        self, metric_name: str, probability_data: list[float]
    ) -> Tuple[list[str], list[list[Any]]]:
        """Prepares data for CSV output with only the required columns."""
        header = [
            "Game",
            "Banner Type",
            "Cumulative Probability",
            "Probability per Roll",
            "First 5 Star Probability",
            "Roll Number",
        ]
        cumulative_probs = self.results.get("cumulative_probabilities", [])
        first_5_star_probs = self.results.get("first_5_star_probabilities", [])
        raw_probs = self.results.get("raw_probabilities", [])
        rolls = self.results.get("rolls", [])
        game = self.game_name
        banner_type = self.banner_type
        def safe_get(lst, idx):
            try:
                return lst[idx]
            except IndexError:
                return None
        rows = []
        for idx, roll in enumerate(rolls):
            cum_prob = safe_get(cumulative_probs, idx)
            prob_per_roll = safe_get(raw_probs, idx)
            first_5_star = safe_get(first_5_star_probs, idx)
            row = [
                game,
                banner_type,
                cum_prob,
                prob_per_roll,
                first_5_star,
                roll,
            ]
            rows.append(row)
        return header, rows

    def save_results_to_csv(self) -> Dict[str, str]:
        """Saves the calculated probability distributions to CSV files.

        Returns:
            Dict[str, str]: A dictionary mapping metric names to their output file paths.
        """
        if not self.results:
            logger.warning(
                f"No results to save for {self.game_name} - {self.banner_type}. Run calculate_probabilities() first."
            )
            return {}

        output_paths: Dict[str, str] = {}

        metrics_to_save = {
            "probability_per_roll": "raw_probabilities",
            "first_5_star_probability": "first_5_star_probabilities",
            "cumulative_probability": "cumulative_probabilities",
        }

        for metric_key, data_key in metrics_to_save.items():
            if data_key in self.results:
                filename = f"csv_output/{self.game_name.lower().replace(' ', '_')}/{self.game_name.lower().replace(' ', '_')}_{self.banner_type.lower().replace(' ', '_')}_{metric_key}.csv"

                # Ensure directory exists (CSVOutputHandler doesn't create dirs)
                # This might be better handled by CSVOutputHandler or a utility function
                import os

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                header, rows = self._prepare_output_data(
                    metric_key, self.results[data_key]
                )
                try:
                    # Write header and data rows only (no metadata row)
                    self.output_handler.write(filename, header, rows)
                    output_paths[metric_key] = filename
                    logger.info(f"Saved {metric_key} to {filename}")
                except Exception as e:
                    logger.error(
                        f"Failed to write {metric_key} to {filename}: {e}",
                        exc_info=True,
                    )
            else:
                logger.warning(
                    f"Data for metric '{data_key}' not found in results for {self.game_name} - {self.banner_type}."
                )

        return output_paths
