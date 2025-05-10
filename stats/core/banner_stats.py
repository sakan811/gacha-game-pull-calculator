"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games (Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations for different banner types.
"""

import os
import numpy as np
import pandas as pd
from core.banner_config import BANNER_CONFIGS
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler


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
        # For config lookup, use the original normalized game_type
        config_game_type = game_type.lower().replace(" ", "_")
        normalized_banner_type = banner_type.lower().replace(" ", "_")

        # Fix: Remove redundant game prefix from banner_type if present
        # e.g., banner_type='rail_light_cone' or 'star_rail_light_cone' -> 'light_cone'
        if config_game_type in ["star_rail", "star"]:
            allowed = ["standard", "limited", "light_cone"]
            for prefix in ["star_rail_", "rail_", "star_"]:
                if normalized_banner_type.startswith(prefix):
                    normalized_banner_type = normalized_banner_type[len(prefix) :]
        elif config_game_type == "genshin":
            allowed = ["standard", "limited", "weapon"]
            if normalized_banner_type.startswith("genshin_"):
                normalized_banner_type = normalized_banner_type[len("genshin_") :]
        elif config_game_type == "zenless":
            allowed = ["standard", "limited", "w_engine", "bangboo"]
            if normalized_banner_type.startswith("zenless_"):
                normalized_banner_type = normalized_banner_type[len("zenless_") :]
        else:
            allowed = []

        if normalized_banner_type not in allowed:
            raise ValueError(
                f"Invalid banner_type '{banner_type}' for game '{game_type}'. Allowed: {allowed}"
            )

        self.banner_type = normalized_banner_type
        # Always use 'star_rail' as config key prefix for both 'star' and 'star_rail'
        if config_game_type in ["star_rail", "star"]:
            self.config_key = f"star_rail_{self.banner_type}"
            self.game_type = "star_rail"
        else:
            self.config_key = f"{config_game_type}_{self.banner_type}"
            self.game_type = config_game_type
        self.config = self._load_config()
        self.rolls = np.arange(1, self.config.hard_pity + 1).tolist()
        self._calculate_all_probabilities()

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
        """Save each calculated metric to its own CSV file in stats/csv_output/<game_type>/ with game and banner in filename.

        This method exports each metric (roll numbers, probability per roll, cumulative probability)
        to a separate CSV file inside the 'stats/csv_output/<game_type>' directory, with filenames including game and banner type.

        Returns:
            dict: Mapping of metric name to saved CSV file path.
        """
        data_df = (
            self._prepare_plot_data()
        )  # Renamed for clarity to avoid conflict with 'data' list
        csv_handler = CSVOutputHandler()
        base_output_dir = os.path.join(os.path.dirname(__file__), "..", "csv_output")
        # Always use 'star_rail' as output dir and prefix for both 'star' and 'star_rail'
        if self.game_type in ["star_rail", "star"]:
            output_dir = os.path.join(base_output_dir, "star_rail")
            prefix = f"star_rail_{self.banner_type}"
        else:
            output_dir = os.path.join(base_output_dir, self.game_type)
            prefix = f"{self.game_type}_{self.banner_type}"
        os.makedirs(output_dir, exist_ok=True)

        file_paths = {}

        # Save roll numbers
        roll_numbers_path = os.path.join(output_dir, f"{prefix}_roll_numbers.csv")
        roll_numbers_header = ["Game", "Banner Type", "Roll Number"]
        roll_numbers_data = data_df[roll_numbers_header].values.tolist()
        csv_handler.write(roll_numbers_path, roll_numbers_header, roll_numbers_data)
        file_paths["roll_numbers"] = roll_numbers_path

        # Save probability per roll
        prob_per_roll_path = os.path.join(
            output_dir, f"{prefix}_probability_per_roll.csv"
        )
        prob_per_roll_header = [
            "Game",
            "Banner Type",
            "Roll Number",
            "Probability per Roll",
        ]
        prob_per_roll_data = data_df[prob_per_roll_header].values.tolist()
        csv_handler.write(prob_per_roll_path, prob_per_roll_header, prob_per_roll_data)
        file_paths["probability_per_roll"] = prob_per_roll_path

        # Save cumulative probability
        cumulative_prob_path = os.path.join(
            output_dir, f"{prefix}_cumulative_probability.csv"
        )
        cumulative_prob_header = [
            "Game",
            "Banner Type",
            "Roll Number",
            "Cumulative Probability",
        ]
        cumulative_prob_data = data_df[cumulative_prob_header].values.tolist()
        csv_handler.write(
            cumulative_prob_path, cumulative_prob_header, cumulative_prob_data
        )
        file_paths["cumulative_probability"] = cumulative_prob_path

        return file_paths

    def _prepare_plot_data(self):
        """Prepare data frame for statistics export, including game and banner type columns.

        Returns:
            pd.DataFrame: Data frame with columns:
                - 'Game': Game type (e.g., 'star_rail')
                - 'Banner Type': Banner type (e.g., 'limited')
                - 'Roll Number': Roll count (1 to hard pity)
                - 'Probability per Roll': First 5★ probability per roll
                - 'Cumulative Probability': Chance of 5★ by that roll
        """
        n = len(self.rolls)
        return pd.DataFrame(
            {
                "Game": [self.game_type] * n,
                "Banner Type": [self.banner_type] * n,
                "Roll Number": self.rolls,
                "Probability per Roll": self.p_first_5_star,
                "Cumulative Probability": self.cumulative_prob,
            }
        )
