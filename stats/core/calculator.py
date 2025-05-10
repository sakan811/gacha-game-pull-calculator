from abc import ABC
from typing import Optional, List
from core.banner import BannerConfig
import numpy as np


class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities."""

    def __init__(self, config: Optional[BannerConfig] = None):
        self.config: Optional[BannerConfig] = config
        self.rolls: List[int] = []
        self.probabilities: List[float] = []  # Raw probabilities for each roll
        self.p_first_5_star: List[float] = [] # Probability of getting the first 5-star on a specific roll
        self.cumulative_prob: List[float] = [] # Cumulative probability of getting a 5-star by a specific roll

        if self.config:
            self._initialize_calculations()

    def _initialize_calculations(self):
        """Calculates and stores all probability arrays based on the config."""
        if not self.config: # Should not happen if called from constructor with config
            return

        self.rolls = [int(x) for x in np.arange(1, self.config.hard_pity + 1)]
        self.probabilities = self._calculate_raw_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob_from_raw(self.probabilities)
        self.cumulative_prob = self._calculate_cumulative_prob_from_raw(self.probabilities)

    def _calculate_raw_probabilities(self) -> List[float]:
        """Calculates the raw probability of success for each roll."""
        if self.config is None:
            raise ValueError("Config must be set to calculate raw probabilities.")

        probabilities_list = []
        for roll in self.rolls:
            if roll < self.config.soft_pity_start_after:
                probabilities_list.append(self.config.base_rate)
            elif roll < self.config.hard_pity:
                # Calculate increased rate during soft pity
                increased_rate = (
                    self.config.base_rate
                    + (roll - self.config.soft_pity_start_after + 1)
                    * self.config.rate_increase
                )
                probabilities_list.append(min(1.0, increased_rate))
            else: # Hard pity
                probabilities_list.append(1.0)
        return probabilities_list

    def _calculate_first_5star_prob_from_raw(self, raw_probabilities: List[float]) -> List[float]:
        """Calculates the probability of obtaining the first 5-star on exactly the k-th roll."""
        p_first_5_star_list = []
        prob_no_5star_so_far = 1.0
        for p_roll in raw_probabilities:
            success_prob_this_roll = prob_no_5star_so_far * p_roll
            p_first_5_star_list.append(success_prob_this_roll)
            prob_no_5star_so_far *= (1 - p_roll)
        return p_first_5_star_list

    def _calculate_cumulative_prob_from_raw(self, raw_probabilities: List[float]) -> List[float]:
        """Calculates the cumulative probability of obtaining at least one 5-star by the k-th roll."""
        cumulative_list = []
        prob_no_5star_at_all = 1.0
        for p_roll in raw_probabilities:
            prob_no_5star_at_all *= (1 - p_roll)
            cumulative_list.append(1 - prob_no_5star_at_all)
        return cumulative_list
