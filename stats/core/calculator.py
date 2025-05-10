from abc import ABC
from typing import Optional, List
from core.banner import BannerConfig
import numpy as np


class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities."""

    def __init__(self, config: Optional[BannerConfig] = None):
        self.config: Optional[BannerConfig] = config
        self.rolls: List[int] = []
        self.probabilities: List[float] = []
        self.p_first_5_star: List[float] = []
        self.cumulative_prob: List[float] = []
        if self.config:
            self._initialize_calculations()

    def _initialize_calculations(self):
        if not self.config:
            return
        self.rolls = [int(x) for x in np.arange(1, self.config.hard_pity + 1)]
        self.probabilities = self._calculate_raw_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob_from_raw(
            self.probabilities
        )
        self.cumulative_prob = self._calculate_cumulative_prob_from_raw(
            self.probabilities
        )

    def _calculate_raw_probabilities(self) -> List[float]:
        if self.config is None:
            raise ValueError("Config must be set to calculate raw probabilities.")
        probabilities_list = []
        for roll in self.rolls:
            if roll < self.config.soft_pity_start_after:
                probabilities_list.append(self.config.base_rate)
            elif roll < self.config.hard_pity:
                increased_rate = (
                    self.config.base_rate
                    + (roll - self.config.soft_pity_start_after + 1)
                    * self.config.rate_increase
                )
                probabilities_list.append(min(1.0, increased_rate))
            else:
                probabilities_list.append(1.0)
        return probabilities_list

    def _calculate_first_5star_prob_from_raw(
        self, raw_probabilities: List[float]
    ) -> List[float]:
        p_first_5_star_list = []
        prob_no_5star_so_far = 1.0
        for p_roll in raw_probabilities:
            success_prob_this_roll = prob_no_5star_so_far * p_roll
            p_first_5_star_list.append(success_prob_this_roll)
            prob_no_5star_so_far *= 1 - p_roll
        return p_first_5_star_list

    def _calculate_cumulative_prob_from_raw(
        self, raw_probabilities: List[float]
    ) -> List[float]:
        cumulative_list = []
        prob_no_5star_at_all = 1.0
        for p_roll in raw_probabilities:
            prob_no_5star_at_all *= 1 - p_roll
            cumulative_list.append(1 - prob_no_5star_at_all)
        return cumulative_list
