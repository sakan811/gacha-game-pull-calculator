from dataclasses import dataclass
from typing import Optional


@dataclass
class BannerConfig:
    """Banner configuration parameters."""

    base_rate: float
    four_star_rate: float
    soft_pity_start_after: int
    hard_pity: int
    rate_increase: float
    guaranteed_rate_up: bool
    rate_up_chance: Optional[float] = None


class BaseBanner:
    """Base class for banner logic."""

    def __init__(self, config: BannerConfig):
        self.config = config

    def get_base_rate(self) -> float:
        """Return the base 5-star rate for the banner."""
        return self.config.base_rate

    def get_hard_pity(self) -> int:
        """Return the hard pity value for the banner."""
        return self.config.hard_pity

    def get_soft_pity_start(self) -> int:
        """Return the roll number where soft pity starts."""
        return self.config.soft_pity_start_after
