"""Main module for HSR Warp Statistics calculation."""
import numpy as np
import pandas as pd

from stats_utils.banner_config import BANNER_CONFIGS
from stats_utils.probability_calculator import ProbabilityCalculator
from stats_utils.visualization import BannerVisualizer


class WarpStats(ProbabilityCalculator):
    def __init__(self, banner_type="standard"):
        """Initialize warp statistics calculator."""
        self.banner_type = banner_type.lower().replace(' ', '_')
        self._load_config()
        self.rolls = np.arange(1, self.hard_pity + 1)
        self._calculate_all_probabilities()
        self.visualizer = BannerVisualizer()

    def _load_config(self):
        """Load banner configuration."""
        if self.banner_type not in BANNER_CONFIGS:
            raise ValueError(
                "banner_type must be 'standard', 'limited', or 'light_cone'"
            )
        config = BANNER_CONFIGS[self.banner_type]
        for key, value in vars(config).items():
            setattr(self, key, value)

    def _calculate_all_probabilities(self):
        """Calculate all probability distributions."""
        self.probabilities = self._calculate_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob()
        self.cumulative_prob = self._calculate_cumulative_prob()

    def plot_statistics(self, save_path=None):
        """Create and display probability plots."""
        data = self._prepare_plot_data()
        self.visualizer.create_plot(data, self.banner_type, save_path)

    def _prepare_plot_data(self):
        """Prepare data for plotting."""
        return pd.DataFrame({
            "Roll Number": self.rolls,
            "Probability per Roll": self.p_first_5_star,
            "Cumulative Probability": self.cumulative_prob,
        })
