from abc import ABC
from typing import Optional
from core.banner import BannerConfig
import numpy as np


class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities."""

    def __init__(self, config: Optional[BannerConfig] = None) -> None:
        self.config: Optional[BannerConfig] = config
        self.rolls: np.ndarray = np.array([])
        self.probabilities: np.ndarray = np.array([])
        self.p_first_5_star: np.ndarray = np.array([])
        self.cumulative_prob: np.ndarray = np.array([])
        if self.config:
            self._initialize_calculations()

    def _initialize_calculations(self) -> None:
        if not self.config:
            return
        self.rolls = np.arange(1, self.config.hard_pity + 1)
        self.probabilities = self._calculate_raw_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob_from_raw(
            self.probabilities
        )
        self.cumulative_prob = self._calculate_cumulative_prob_from_raw(
            self.probabilities
        )

    def _calculate_raw_probabilities(self) -> np.ndarray:
        if self.config is None:
            raise ValueError("Config must be set to calculate raw probabilities.")
        rolls = self.rolls
        base_rate = self.config.base_rate
        soft_pity = self.config.soft_pity_start_after
        hard_pity = self.config.hard_pity
        rate_increase = self.config.rate_increase

        probs = np.full_like(rolls, base_rate, dtype=np.float64)
        soft_mask = (rolls >= soft_pity) & (rolls < hard_pity)
        probs[soft_mask] = np.minimum(
            1.0, base_rate + (rolls[soft_mask] - soft_pity + 1) * rate_increase
        )
        probs[rolls == hard_pity] = 1.0
        return probs

    def _calculate_first_5star_prob_from_raw(
        self, raw_probabilities: np.ndarray
    ) -> np.ndarray:
        p_first_5_star = np.zeros_like(raw_probabilities)
        prob_no_5star_so_far = 1.0
        for i, p_roll in enumerate(raw_probabilities):
            p_first_5_star[i] = prob_no_5star_so_far * p_roll
            prob_no_5star_so_far *= 1 - p_roll
        return p_first_5_star

    def _calculate_cumulative_prob_from_raw(
        self, raw_probabilities: np.ndarray
    ) -> np.ndarray:
        cumulative = np.zeros_like(raw_probabilities)
        prob_no_5star_at_all = 1.0
        for i, p_roll in enumerate(raw_probabilities):
            prob_no_5star_at_all *= 1 - p_roll
            cumulative[i] = 1 - prob_no_5star_at_all
        return cumulative
