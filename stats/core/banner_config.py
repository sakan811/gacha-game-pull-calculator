"""Configuration for different banner types."""

from core.banner import BannerConfig

# Banner configurations for all games and banner types
BANNER_CONFIGS = {
    # Star Rail banners
    "star_rail_standard": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.0,
    ),
    "star_rail_limited": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    ),
    "star_rail_light_cone": BannerConfig(
        base_rate=0.008,
        four_star_rate=0.066,
        soft_pity_start_after=65,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    ),
    # Genshin banners
    "genshin_standard": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.0,
    ),
    "genshin_limited": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    ),
    "genshin_weapon": BannerConfig(
        base_rate=0.007,
        four_star_rate=0.066,
        soft_pity_start_after=62,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    ),
    # Zenless Zone Zero banners
    "zenless_standard": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.0,
    ),
    "zenless_limited": BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    ),
    "zenless_w_engine": BannerConfig(
        base_rate=0.01,
        four_star_rate=0.08,
        soft_pity_start_after=64,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    ),
    "zenless_bangboo": BannerConfig(
        base_rate=0.01,
        four_star_rate=0.051,
        soft_pity_start_after=64,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=1.0,
    ),
}
