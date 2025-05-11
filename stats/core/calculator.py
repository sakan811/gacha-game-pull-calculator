"""Probability calculator for gacha banners."""


class ProbabilityCalculator:
    """Calculates banner probabilities."""

    def __init__(self, config):
        self.config = config

    def calculate_probabilities(self) -> tuple[list[float], list[float], list[float]]:
        """Calculate and return probabilities for all rolls.

        Returns:
            tuple: (per_roll_prob, cumulative_prob, first_5star_prob)
        """
        base_prob = self.config.base_rate
        soft_pity = self.config.soft_pity_start_after

        per_roll = [base_prob] * soft_pity
        cumulative = [1 - (1 - base_prob) ** (i + 1) for i in range(soft_pity)]
        first_5star = [base_prob * (1 - base_prob) ** i for i in range(soft_pity)]

        return per_roll, cumulative, first_5star
