"""Module for calculating banner probabilities."""

class ProbabilityCalculator:
    def _calculate_probabilities(self):
        """Calculate base probabilities for each roll."""
        probabilities = []
        for roll in self.rolls:
            if roll < self.pity_start:
                probabilities.append(self.base_rate)
            elif roll < self.hard_pity:
                # Calculate increased rate after soft pity
                increased_rate = (
                    self.base_rate + (roll - self.pity_start + 1) * self.rate_increase
                )
                probabilities.append(min(1.0, increased_rate))
            else:
                probabilities.append(1.0)  # Hard pity
        return probabilities

    def _calculate_first_5star_prob(self):
        """Calculate probability of getting first 5★ specifically on each roll."""
        p_first_5_star = []
        prob_no_5star = 1.0
        
        for p in self.probabilities:
            # Probability of getting 5★ on this roll = 
            # Probability of not getting 5★ before * Probability of getting 5★ on this roll
            success_prob = prob_no_5star * p
            p_first_5_star.append(success_prob)
            prob_no_5star *= (1 - p)
            
        return p_first_5_star

    def _calculate_cumulative_prob(self):
        """Calculate cumulative probability of getting at least one 5★."""
        cumulative = []
        prob_no_5star = 1.0
        
        for p in self.probabilities:
            prob_no_5star *= (1 - p)
            cumulative.append(1 - prob_no_5star)
            
        return cumulative 