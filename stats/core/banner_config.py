"""Configuration for different banner types."""

from core.banner import BannerConfig

BANNER_CONFIGS = {
    "star_rail_standard": BannerConfig(
        game_name="Star Rail",  # Added
        banner_type="Standard",  # Added
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.5,
    ),
    "star_rail_limited": BannerConfig(
        game_name="Star Rail",
        banner_type="Limited",  # Updated
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    ),
    "star_rail_light_cone": BannerConfig(
        game_name="Star Rail",  # Added
        banner_type="Light Cone",  # Added
        base_rate=0.008,
        four_star_rate=0.066,
        soft_pity_start_after=65,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    ),
    "genshin_standard": BannerConfig(
        game_name="Genshin Impact",  # Added
        banner_type="Standard",  # Added
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.5,
    ),
    "genshin_limited": BannerConfig(
        game_name="Genshin Impact",
        banner_type="Limited",  # Updated
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    ),
    "genshin_weapon": BannerConfig(
        game_name="Genshin Impact",  # Added
        banner_type="Weapon",  # Added
        base_rate=0.007,
        four_star_rate=0.066,
        soft_pity_start_after=62,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    ),
    "zenless_standard": BannerConfig(
        game_name="Zenless Zone Zero",  # Added
        banner_type="Standard",  # Added
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.5,
    ),
    "zenless_limited": BannerConfig(
        game_name="Zenless Zone Zero",
        banner_type="Limited",  # Updated
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    ),
    "zenless_w_engine": BannerConfig(
        game_name="Zenless Zone Zero",  # Added
        banner_type="W-Engine",  # Added
        base_rate=0.01,
        four_star_rate=0.08,
        soft_pity_start_after=64,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    ),
    "zenless_bangboo": BannerConfig(
        game_name="Zenless Zone Zero",  # Added
        banner_type="Bangboo",  # Added
        base_rate=0.01,
        four_star_rate=0.051,
        soft_pity_start_after=64,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=1.0,
    ),
}
