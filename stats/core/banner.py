"""Banner configuration for probability calculations."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class BannerConfig:
    """Configuration for banner probability calculations."""
    game_name: str
    banner_type: str
    base_rate: float
    soft_pity_start: int
    hard_pity: int
    rate_increase: float
    guaranteed: bool

BANNER_CONFIGS = {
    "StarRail": {
        "Standard": BannerConfig(
            game_name="StarRail",
            banner_type="Standard",
            base_rate=0.006,
            soft_pity_start=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed=False
        ),
        "Limited": BannerConfig(
            game_name="StarRail",
            banner_type="Limited",
            base_rate=0.006,
            soft_pity_start=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed=True
        )
    }
}
