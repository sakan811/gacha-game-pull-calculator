"""Simplified probability calculator for banners."""

from dataclasses import dataclass
from core.common.logging import get_logger

@dataclass
class ProbabilityResult:
    base_prob: float
    cumulative_prob: float
    soft_pity_start: int

class ProbabilityCalculator:
    """Handles probability calculations for banners."""

    def __init__(self, config):
        self.logger = get_logger(__name__)
        self.config = config

    def calculate(self) -> ProbabilityResult:
        """Calculate probability metrics for banner."""
        base_prob = self.config.base_rate
        cumulative = self._calculate_cumulative_prob(base_prob)
        return ProbabilityResult(
            base_prob=base_prob,
            cumulative_prob=cumulative,
            soft_pity_start=self.config.soft_pity_start
        )

    def _calculate_cumulative_prob(self, base_prob: float) -> float:
        """Calculate cumulative probability for banner."""
        return 1 - (1 - base_prob) ** self.config.soft_pity_start
