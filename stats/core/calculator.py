"""Probability calculator for gacha banners."""

from typing import List, Tuple


class ProbabilityCalculator:
    """Calculates banner probabilities."""

    def __init__(self, config):
        self.config = config

    def calculate_probabilities(self) -> Tuple[List[float], List[float], List[float]]:
        """Calculate and return probabilities for all rolls.

        Calculates three types of probabilities:
        1. Per roll probability: Chance of getting 5* on that specific roll
        2. Cumulative probability: Chance of getting at least one 5* by that roll
        3. First 5* probability: Chance of getting first 5* exactly on that roll

        Returns:
            tuple: (per_roll_prob, cumulative_prob, first_5star_prob)
        """
        base_rate = self.config.base_rate
        soft_pity_start = self.config.soft_pity_start_after
        hard_pity = self.config.hard_pity
        rate_increase = self.config.rate_increase

        # Calculate per roll probabilities
        per_roll = []
        for i in range(hard_pity):
            roll_number = i + 1  # Convert 0-based index to 1-based roll number

            if roll_number <= soft_pity_start:
                prob = base_rate
            elif roll_number == hard_pity:
                prob = 1.0  # Hard pity
            else:
                # Apply the rate increase formula during soft pity
                rolls_into_soft_pity = roll_number - soft_pity_start
                prob = min(1.0, base_rate + (rate_increase * rolls_into_soft_pity))
            per_roll.append(prob)

        # Calculate first 5* probability (chance to get first 5* on exactly this roll)
        first_5star = []
        no_5star_prob = 1.0
        for prob in per_roll:
            first_5star.append(no_5star_prob * prob)
            no_5star_prob *= 1.0 - prob

        # Calculate cumulative probability (chance to get at least one 5* by this roll)
        cumulative = []
        running_prob = 0.0
        for prob in first_5star:
            running_prob += prob
            cumulative.append(running_prob)

        return per_roll, cumulative, first_5star
