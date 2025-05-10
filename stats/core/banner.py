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
