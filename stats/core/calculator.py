from abc import ABC
from typing import Optional
from core.banner import BannerConfig

class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities."""

    def __init__(self):
        self.probabilities: list[float] = []
        self.rolls: list[int] = []
        self.config: Optional[BannerConfig] = None

    def _calculate_probabilities(self):
        if self.config is None:
            raise ValueError(
                "config must be set to a BannerConfig before calling _calculate_probabilities"
            )
        probabilities = []
        for roll in self.rolls:
            if roll < self.config.soft_pity_start_after:
                probabilities.append(self.config.base_rate)
            elif roll < self.config.hard_pity:
                increased_rate = (
                    self.config.base_rate
                    + (roll - self.config.soft_pity_start_after + 1)
                    * self.config.rate_increase
                )
                probabilities.append(min(1.0, increased_rate))
            else:
                probabilities.append(1.0)
        return probabilities

    def _calculate_first_5star_prob(self):
        p_first_5_star = []
        prob_no_5star = 1.0
        for p in self.probabilities:
            success_prob = prob_no_5star * p
            p_first_5_star.append(success_prob)
            prob_no_5star *= 1 - p
        return p_first_5_star

    def _calculate_cumulative_prob(self):
        cumulative = []
        prob_no_5star = 1.0
        for p in self.probabilities:
            prob_no_5star *= 1 - p
            cumulative.append(1 - prob_no_5star)
        return cumulative
