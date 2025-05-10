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
        parsed_game_type, parsed_banner_type = self._parse_and_validate_game_banner(
            game_type, banner_type
        )

        self.banner_type = parsed_banner_type
        self.game_type = parsed_game_type 

        if self.game_type == "star_rail":
            self.config_key = f"star_rail_{self.banner_type}"
        else:
            self.config_key = f"{self.game_type}_{self.banner_type}"
            
        config = self._load_config()
        
        super().__init__(config)

    def _parse_and_validate_game_banner(self, game_type: str, banner_type: str) -> tuple[str, str]:
        """
        Normalizes and validates game_type and banner_type.
        Returns the processed and standardized game_type and banner_type.
        """
        processed_game_type = game_type.lower().replace(" ", "_")
        processed_banner_type = banner_type.lower().replace(" ", "_")

        game_specific_banner_types = {
            "star_rail": {"allowed": ["standard", "limited", "light_cone"], "prefixes": ["star_rail_", "rail_", "star_"], "output_name": "star_rail"},
            "star": {"allowed": ["standard", "limited", "light_cone"], "prefixes": ["star_rail_", "rail_", "star_"], "output_name": "star_rail"}, 
            "genshin": {"allowed": ["standard", "limited", "weapon"], "prefixes": ["genshin_"], "output_name": "genshin"},
            "zenless": {"allowed": ["standard", "limited", "w_engine", "bangboo"], "prefixes": ["zenless_"], "output_name": "zenless"},
        }

        if processed_game_type not in game_specific_banner_types:
            raise ValueError(
                f"Unsupported game_type: '{game_type}'. Supported: {list(game_specific_banner_types.keys())}"
            )

        details = game_specific_banner_types[processed_game_type]
        allowed_banners = details["allowed"]
        standardized_game_name = details["output_name"]
        
        # Strip prefixes from banner_type
        for prefix in details["prefixes"]:
            if processed_banner_type.startswith(prefix):
                processed_banner_type = processed_banner_type[len(prefix):]
                break 

        if processed_banner_type not in allowed_banners:
            raise ValueError(
                f"Invalid banner_type '{banner_type}' for game '{game_type}'. Allowed for {standardized_game_name}: {allowed_banners}"
            )
            
        return standardized_game_name, processed_banner_type

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

    def save_statistics_csv(self):
        """Save each calculated metric to its own CSV file in stats/csv_output/<game_type>/ with game and banner in filename.

        This method exports each metric (roll numbers, probability per roll, cumulative probability)
        to a separate CSV file inside the 'stats/csv_output/<game_type>' directory, with filenames including game and banner type.

        Returns:
            dict: Mapping of metric name to saved CSV file path.
        """
        data_df = (
            self._prepare_plot_data()
        )
        csv_handler = CSVOutputHandler()
        base_output_dir = os.path.join(os.path.dirname(__file__), "..", "csv_output")
        
        if self.game_type == "star_rail":
            output_dir = os.path.join(base_output_dir, "star_rail")
            prefix = f"star_rail_{self.banner_type}"
        else:
            output_dir = os.path.join(base_output_dir, self.game_type)
            prefix = f"{self.game_type}_{self.banner_type}"
        os.makedirs(output_dir, exist_ok=True)

        file_paths = {}

        roll_numbers_path = os.path.join(output_dir, f"{prefix}_roll_numbers.csv")
        roll_numbers_header = ["Game", "Banner Type", "Roll Number"]
        roll_numbers_data = data_df[roll_numbers_header].values.tolist()
        csv_handler.write(roll_numbers_path, roll_numbers_header, roll_numbers_data)
        file_paths["roll_numbers"] = roll_numbers_path

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
