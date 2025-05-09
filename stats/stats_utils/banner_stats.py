"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games (Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations for different banner types.
"""

import os
import numpy as np
import pandas as pd

from stats_utils.banner_config import BANNER_CONFIGS
from stats_utils.probability_calculator import ProbabilityCalculator


class BannerStats(ProbabilityCalculator):
    """Class for calculating gacha banner statistics.

    This class extends ProbabilityCalculator to provide game-specific banner analysis. It handles configuration loading and probability calculations for different banner types across games.
    """

    def __init__(self, game_type="star_rail", banner_type="standard"):
        """Initialize banner statistics calculator with game and banner settings.

        Args:
            game_type (str): Type of game to analyze. Options:
                - 'star_rail': Honkai: Star Rail
                - 'genshin': Genshin Impact
                - 'zenless': Zenless Zone Zero
            banner_type (str): Type of banner to analyze. Options vary by game:
                - Star Rail: 'standard', 'limited', 'light_cone'
                - Genshin: 'standard', 'limited', 'weapon'
                - Zenless: 'standard', 'limited', 'w_engine', 'bangboo'

        Raises:
            ValueError: If game_type or banner_type is not supported
        """
        self.game_type = game_type.lower().replace(" ", "_")
        self.banner_type = banner_type.lower().replace(" ", "_")
        self.config_key = f"{self.game_type}_{self.banner_type}"
        self.config = self._load_config()
        self.rolls = np.arange(1, self.config.hard_pity + 1)
        self._calculate_all_probabilities()
        # Visualization logic removed

    def _load_config(self):
        """Load banner configuration for the specified game and banner type.

        This method retrieves the appropriate configuration settings including
        base rates, soft pity, and hard pity values for the selected banner.

        Returns:
            BannerConfig: Configuration settings for the selected banner type

        Raises:
            ValueError: If the combination of game_type and banner_type is invalid
        """
        if self.config_key not in BANNER_CONFIGS:
            valid_configs = list(BANNER_CONFIGS.keys())
            raise ValueError(
                f"Invalid configuration key: {self.config_key}. Valid keys are: {valid_configs}"
            )
        return BANNER_CONFIGS[self.config_key]

    def _calculate_all_probabilities(self):
        """Calculate all probability distributions for the banner.

        Computes three probability distributions:
        1. Base probabilities for each roll
        2. Probability of getting first 5★ on each roll
        3. Cumulative probability of getting at least one 5★
        """
        self.probabilities = self._calculate_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob()
        self.cumulative_prob = self._calculate_cumulative_prob()

    def save_statistics_csv(self):
        """Save each calculated metric to its own CSV file in stats/csv_output/ with game and banner in filename.

        This method exports each metric (roll numbers, probability per roll, cumulative probability)
        to a separate CSV file inside the 'stats/csv_output' directory, with filenames including game and banner type.

        Returns:
            dict: Mapping of metric name to saved CSV file path.
        """
        data = self._prepare_plot_data()
        output_dir = os.path.join(os.path.dirname(__file__), "..", "csv_output")
        os.makedirs(output_dir, exist_ok=True)

        prefix = f"{self.game_type}_{self.banner_type}"
        file_paths = {}

        roll_numbers_path = os.path.join(output_dir, f"{prefix}_roll_numbers.csv")
        data[["Roll Number"]].to_csv(roll_numbers_path, index=False)
        file_paths["roll_numbers"] = roll_numbers_path

        prob_per_roll_path = os.path.join(output_dir, f"{prefix}_probability_per_roll.csv")
        data[["Probability per Roll"]].to_csv(prob_per_roll_path, index=False)
        file_paths["probability_per_roll"] = prob_per_roll_path

        cumulative_prob_path = os.path.join(output_dir, f"{prefix}_cumulative_probability.csv")
        data[["Cumulative Probability"]].to_csv(cumulative_prob_path, index=False)
        file_paths["cumulative_probability"] = cumulative_prob_path

        return file_paths

    def _prepare_plot_data(self):
        """Prepare data frame for statistics export.

        Creates a pandas DataFrame containing:
        - Roll numbers (1 to hard pity)
        - Probability of getting first 5★ on each roll
        - Cumulative probability of getting 5★ by each roll

        Returns:
            pd.DataFrame: Data frame with columns:
                - 'Roll Number': Roll count (1 to hard pity)
                - 'Probability per Roll': First 5★ probability per roll
                - 'Cumulative Probability': Chance of 5★ by that roll
        """
        return pd.DataFrame(
            {
                "Roll Number": self.rolls,
                "Probability per Roll": self.p_first_5_star,
                "Cumulative Probability": self.cumulative_prob,
            }
        )
