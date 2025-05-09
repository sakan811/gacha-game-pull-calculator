"""Module for calculating gacha banner probabilities.

This module implements the core probability calculations for gacha banner systems,
including base rates, soft pity, and hard pity mechanics.
"""

from abc import ABC
from typing import Optional
from stats_utils.banner_config import BannerConfig


class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities.

    This class provides methods to calculate various probability distributions
    for gacha banner systems, including:
    - Base probability calculations with soft and hard pity
    - First 5-star pull probability distribution
    - Cumulative probability of obtaining a 5-star
    """

    def __init__(self):
        """Initialize ProbabilityCalculator with default attributes.

        Attributes:
            probabilities (list): Probability of 5★ for each roll (to be set by subclass).
            rolls (list or None): List of roll numbers (to be set by subclass).
            config (Any or None): Banner configuration object (to be set by subclass).
        """
        self.probabilities: list[float] = []
        self.rolls: list[int] = []
        self.config: Optional[BannerConfig] = None

    def _calculate_probabilities(self):
        """Calculate base probabilities for each roll.

        This method implements the core probability calculation considering:
        1. Base rate before soft pity
        2. Increased rates during soft pity (linear increase)
        3. Guaranteed pull at hard pity

        Returns:
            list: Probability of getting a 5-star for each roll number
        """
        if self.config is None:
            raise ValueError(
                "config must be set to a BannerConfig before calling _calculate_probabilities"
            )
        probabilities = []
        for roll in self.rolls:
            if roll < self.config.soft_pity_start_after:
                probabilities.append(self.config.base_rate)
            elif roll < self.config.hard_pity:
                # Calculate increased rate after soft pity
                increased_rate = (
                    self.config.base_rate
                    + (roll - self.config.soft_pity_start_after + 1)
                    * self.config.rate_increase
                )
                probabilities.append(min(1.0, increased_rate))
            else:
                probabilities.append(1.0)  # Hard pity
        return probabilities

    def _calculate_first_5star_prob(self):
        """Calculate probability of getting first 5★ specifically on each roll.

        This method calculates the probability of getting the first 5-star character/weapon
        exactly on a specific roll number, considering all previous failed attempts.
        The calculation follows the formula:
        P(first 5★ on roll n) = P(no 5★ in rolls 1 to n-1) * P(5★ on roll n)

        Returns:
            list: Probability of getting first 5★ on each specific roll number
        """
        p_first_5_star = []
        prob_no_5star = 1.0

        for p in self.probabilities:
            # Probability of getting 5★ on this roll =
            # Probability of not getting 5★ before * Probability of getting 5★ on this roll
            success_prob = prob_no_5star * p
            p_first_5_star.append(success_prob)
            prob_no_5star *= 1 - p

        return p_first_5_star

    def _calculate_cumulative_prob(self):
        """Calculate cumulative probability of getting at least one 5★.

        This method calculates the probability of having obtained at least one
        5-star by a certain roll number. It uses the complement of the probability
        of getting no 5-stars in all rolls up to that point:
        P(at least one 5★ by roll n) = 1 - P(no 5★ in rolls 1 to n)

        Returns:
            list: Cumulative probability of getting at least one 5★ by each roll number
        """
        cumulative = []
        prob_no_5star = 1.0

        for p in self.probabilities:
            prob_no_5star *= 1 - p
            cumulative.append(1 - prob_no_5star)

        return cumulative
