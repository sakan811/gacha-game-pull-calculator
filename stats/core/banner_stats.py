"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games (Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations for different banner types.
"""

import os
import pandas as pd  # numpy is used by calculator, not directly here
from typing import Dict, Tuple, Any, Optional  # Added Optional

from core.banner import BannerConfig  # Corrected import
from core.banner_config import BANNER_CONFIGS
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler

# Define a more structured way to handle game and banner type validation
GAME_BANNER_MAPPING: Dict[str, Dict[str, Any]] = {
    "star_rail": {
        "allowed_banners": ["standard", "limited", "light_cone"],
        "prefixes_to_strip": ["star_rail_", "rail_", "star_"],
        "output_name": "star_rail",
    },
    "star": {  # Alias for star_rail for flexibility in input
        "allowed_banners": ["standard", "limited", "light_cone"],
        "prefixes_to_strip": ["star_rail_", "rail_", "star_"],
        "output_name": "star_rail",
    },
    "genshin": {
        "allowed_banners": ["standard", "limited", "weapon"],
        "prefixes_to_strip": ["genshin_"],
        "output_name": "genshin",
    },
    "zenless": {
        "allowed_banners": ["standard", "limited", "w_engine", "bangboo"],
        "prefixes_to_strip": ["zenless_"],
        "output_name": "zenless",
    },
}


class BannerStats:
    """Orchestrates gacha banner statistics calculation and output for a specific game and banner type.

    This class loads the appropriate configuration, utilizes ProbabilityCalculator
    for core calculations, and manages the output of the results.
    """

    def __init__(self, game_type: str = "star_rail", banner_type: str = "standard"):
        """
        Initializes BannerStats with a specific game and banner type.

        Args:
            game_type: The name of the game (e.g., 'star_rail', 'genshin').
            banner_type: The type of banner (e.g., 'standard', 'limited').

        Raises:
            ValueError: If the game_type or banner_type is unsupported or invalid.
        """
        self.game_type, self.banner_type = self._parse_and_validate_game_banner(
            game_type, banner_type
        )
        self.config_key: str = f"{self.game_type}_{self.banner_type}"
        self.config: BannerConfig = self._load_config()
        self.calculator: ProbabilityCalculator = ProbabilityCalculator(self.config)

    def _parse_and_validate_game_banner(
        self, game_type_input: str, banner_type_input: str
    ) -> Tuple[str, str]:
        """
        Normalizes, validates, and standardizes game_type and banner_type inputs.

        Args:
            game_type_input: The raw game type string.
            banner_type_input: The raw banner type string.

        Returns:
            A tuple containing the standardized game_type and banner_type.

        Raises:
            ValueError: If inputs are invalid or unsupported.
        """
        processed_game_type = game_type_input.lower().replace(" ", "_")
        processed_banner_type = banner_type_input.lower().replace(" ", "_")

        if processed_game_type not in GAME_BANNER_MAPPING:
            raise ValueError(
                f"Unsupported game_type: '{game_type_input}'. Supported: {list(GAME_BANNER_MAPPING.keys())}"
            )

        game_details = GAME_BANNER_MAPPING[processed_game_type]
        standardized_game_name = game_details["output_name"]
        allowed_banners = game_details["allowed_banners"]

        # Strip common prefixes from banner_type to get the core type
        for prefix in game_details["prefixes_to_strip"]:
            if processed_banner_type.startswith(prefix):
                processed_banner_type = processed_banner_type[len(prefix) :]
                break

        if processed_banner_type not in allowed_banners:
            raise ValueError(
                f"Invalid banner_type '{banner_type_input}' for game '{standardized_game_name}'. "
                f"Allowed for {standardized_game_name}: {allowed_banners}"
            )

        return standardized_game_name, processed_banner_type

    def _load_config(self) -> BannerConfig:
        """Loads the banner configuration for the initialized game and banner type.

        Returns:
            BannerConfig: The configuration object for the banner.

        Raises:
            ValueError: If no configuration is found for the config_key.
        """
        if self.config_key not in BANNER_CONFIGS:
            valid_configs = list(BANNER_CONFIGS.keys())
            raise ValueError(
                f"Invalid configuration key: {self.config_key}. Valid keys are: {valid_configs}"
            )
        return BANNER_CONFIGS[self.config_key]

    def get_statistics_dataframe(self) -> pd.DataFrame:
        """Prepares a DataFrame with all relevant statistics for the banner.

        Returns:
            pd.DataFrame: DataFrame containing columns for Game, Banner Type, Roll Number,
                          Probability per Roll, and Cumulative Probability.
        """
        if not self.calculator.rolls:  # Ensure calculator has run
            # This should ideally not be needed if calculator initializes on creation
            # but as a safeguard:
            self.calculator._initialize_calculations()

        num_rolls = len(self.calculator.rolls)
        return pd.DataFrame(
            {
                "Game": [self.game_type] * num_rolls,
                "Banner Type": [self.banner_type] * num_rolls,
                "Roll Number": self.calculator.rolls,
                "Probability per Roll": self.calculator.p_first_5_star,
                "Cumulative Probability": self.calculator.cumulative_prob,
            }
        )

    def save_statistics_csv(
        self, base_output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """Saves calculated banner statistics to CSV files.

        Each key metric (roll numbers, probability per roll, cumulative probability)
        is saved to its own CSV file within a game-specific subdirectory.

        Args:
            base_output_dir: Optional base directory for CSV output.
                             Defaults to 'stats/csv_output/'.

        Returns:
            Dict[str, str]: A dictionary mapping metric names to their saved CSV file paths.
        """
        stats_df = self.get_statistics_dataframe()
        csv_handler = CSVOutputHandler()

        if base_output_dir is None:
            base_output_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "csv_output"
            )

        output_dir = os.path.join(base_output_dir, self.game_type)
        os.makedirs(output_dir, exist_ok=True)

        file_prefix = f"{self.game_type}_{self.banner_type}"
        file_paths: Dict[str, str] = {}

        metrics_to_save = {
            "roll_numbers": ["Game", "Banner Type", "Roll Number"],
            "probability_per_roll": [
                "Game",
                "Banner Type",
                "Roll Number",
                "Probability per Roll",
            ],
            "cumulative_probability": [
                "Game",
                "Banner Type",
                "Roll Number",
                "Cumulative Probability",
            ],
        }

        for metric_name, columns in metrics_to_save.items():
            file_path = os.path.join(output_dir, f"{file_prefix}_{metric_name}.csv")
            data_to_write = stats_df[
                [col for col in columns if col in stats_df.columns]
            ]
            csv_handler.write(
                file_path, list(data_to_write.columns), data_to_write.values.tolist()
            )
            file_paths[metric_name] = file_path

        return file_paths
