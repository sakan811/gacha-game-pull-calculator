"""Configuration for different banner types."""
from dataclasses import dataclass

@dataclass
class BannerConfig:
    """Banner configuration parameters."""
    base_rate: float
    four_star_rate: float
    pity_start: int
    hard_pity: int
    rate_increase: float
    guarantee_featured: bool
    featured_rate: float = None

BANNER_CONFIGS = {
    "standard": BannerConfig(
        base_rate=0.003,
        four_star_rate=0.051,
        pity_start=74,
        hard_pity=90,
        rate_increase=0.06,
        guarantee_featured=False
    ),
    "limited": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        pity_start=74,
        hard_pity=90,
        rate_increase=0.06,
        guarantee_featured=True,
        featured_rate=0.5
    ),
    "light_cone": BannerConfig(
        base_rate=0.008,
        four_star_rate=0.066,
        pity_start=65,
        hard_pity=80,
        rate_increase=0.07,
        guarantee_featured=True,
        featured_rate=0.75
    )
} 