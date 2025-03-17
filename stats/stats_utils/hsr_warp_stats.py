"""Main module for HSR Warp Statistics calculation."""

import numpy as np
import pandas as pd

from stats_utils.banner_config import BANNER_CONFIGS
from stats_utils.probability_calculator import ProbabilityCalculator
from stats_utils.visualization import BannerVisualizer


class WarpStats(ProbabilityCalculator):
    """Class for calculating and visualizing warp statistics."""

    def __init__(self, game_type="star_rail", banner_type="standard"):
        """Initialize warp statistics calculator.

        Args:
            game_type (str): Type of game ('star_rail', 'genshin', or 'zenless')
            banner_type (str): Type of banner. Available types per game:
                - Star Rail: 'standard', 'limited', 'light_cone'
                - Genshin: 'standard', 'limited', 'weapon'
                - Zenless: 'standard', 'limited', 'w_engine', 'bangboo'

        Raises:
            ValueError: If game_type or banner_type is not valid
        """
        self.game_type = game_type.lower().replace(" ", "_")
        self.banner_type = banner_type.lower().replace(" ", "_")
        self.config_key = f"{self.game_type}_{self.banner_type}"
        self.config = self._load_config()
        self.rolls = np.arange(1, self.config.hard_pity + 1)
        self._calculate_all_probabilities()
        self.visualizer = BannerVisualizer()

    def _load_config(self):
        """Load banner configuration.

        Returns:
            BannerConfig: The configuration for the selected banner type

        Raises:
            ValueError: If banner_type is not valid
        """
        if self.config_key not in BANNER_CONFIGS:
            valid_configs = list(BANNER_CONFIGS.keys())
            raise ValueError(
                f"Invalid configuration key: {self.config_key}. Valid keys are: {valid_configs}"
            )
        return BANNER_CONFIGS[self.config_key]

    def _calculate_all_probabilities(self):
        """Calculate all probability distributions."""
        self.probabilities = self._calculate_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob()
        self.cumulative_prob = self._calculate_cumulative_prob()

    def plot_statistics(self, save_path=None):
        """Create and display probability plots.

        Args:
            save_path (str, optional): Path to save the plots. If None, plots are not saved.

        Returns:
            tuple: Tuple containing the distribution and cumulative plots
        """
        data = self._prepare_plot_data()
        self.visualizer.create_plots(data, self.game_type, self.banner_type, save_path)

    def _prepare_plot_data(self):
        """Prepare data for plotting.

        Returns:
            pd.DataFrame: DataFrame containing roll numbers and probabilities
        """
        return pd.DataFrame(
            {
                "Roll Number": self.rolls,
                "Probability per Roll": self.p_first_5_star,
                "Cumulative Probability": self.cumulative_prob,
            }
        )
