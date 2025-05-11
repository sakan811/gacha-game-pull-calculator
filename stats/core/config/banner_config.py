from dataclasses import dataclass
from typing import Dict, Final, Optional
from stats.core.common.errors import ValidationError

GAME_TYPES: Final[set[str]] = {"Star Rail", "Genshin Impact", "Zenless Zone Zero"}
BANNER_TYPES_BY_GAME: Final[Dict[str, set[str]]] = {
    "Star Rail": {"Standard", "Limited", "Light Cone"},
    "Genshin Impact": {"Standard", "Limited", "Weapon"},
    "Zenless Zone Zero": {"Standard", "Limited", "W-Engine", "Bangboo"},
}


@dataclass(frozen=True)
class BannerConfig:
    game_name: str
    banner_type: str
    base_rate: float
    four_star_rate: float
    soft_pity_start_after: int
    hard_pity: int
    rate_increase: float
    guaranteed_rate_up: bool
    rate_up_chance: Optional[float] = None

    def __post_init__(self):
        if self.game_name not in GAME_TYPES:
            raise ValidationError(f"Invalid game name: {self.game_name}")
        valid_types = BANNER_TYPES_BY_GAME.get(self.game_name, set())
        if self.banner_type not in valid_types:
            raise ValidationError(f"Invalid banner type: {self.banner_type}")
        if not (0.0 <= self.base_rate <= 1.0):
            raise ValidationError("Base rate must be between 0 and 1")
        if not (0.0 <= self.four_star_rate <= 1.0):
            raise ValidationError("Four star rate must be between 0 and 1")
        if not (1 <= self.soft_pity_start_after <= self.hard_pity <= 200):
            raise ValidationError("Invalid pity values")
        if not (0.0 <= self.rate_increase <= 1.0):
            raise ValidationError("Rate increase must be between 0 and 1")
        if self.rate_up_chance is not None and not (0 <= self.rate_up_chance <= 1):
            raise ValidationError("Rate up chance must be between 0 and 1")


BANNER_CONFIGS = {
    "Star Rail": {
        "standard": BannerConfig(
            game_name="Star Rail",
            banner_type="Standard",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=False,
            rate_up_chance=0.5,
        ),
        "limited": BannerConfig(
            game_name="Star Rail",
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=0.5,
        ),
        "light_cone": BannerConfig(
            game_name="Star Rail",
            banner_type="Light Cone",
            base_rate=0.008,
            four_star_rate=0.066,
            soft_pity_start_after=65,
            hard_pity=80,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=0.75,
        ),
    },
    "Genshin Impact": {
        "standard": BannerConfig(
            game_name="Genshin Impact",
            banner_type="Standard",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=False,
            rate_up_chance=0.5,
        ),
        "limited": BannerConfig(
            game_name="Genshin Impact",
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=0.5,
        ),
        "weapon": BannerConfig(
            game_name="Genshin Impact",
            banner_type="Weapon",
            base_rate=0.007,
            four_star_rate=0.066,
            soft_pity_start_after=62,
            hard_pity=80,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=0.75,
        ),
    },
    "Zenless Zone Zero": {
        "standard": BannerConfig(
            game_name="Zenless Zone Zero",
            banner_type="Standard",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=False,
            rate_up_chance=0.5,
        ),
        "limited": BannerConfig(
            game_name="Zenless Zone Zero",
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=0.5,
        ),
        "w_engine": BannerConfig(
            game_name="Zenless Zone Zero",
            banner_type="W-Engine",
            base_rate=0.01,
            four_star_rate=0.08,
            soft_pity_start_after=64,
            hard_pity=80,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=0.75,
        ),
        "bangboo": BannerConfig(
            game_name="Zenless Zone Zero",
            banner_type="Bangboo",
            base_rate=0.01,
            four_star_rate=0.051,
            soft_pity_start_after=64,
            hard_pity=80,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=1.0,
        ),
    },
}
