"""Banner configuration module with validation."""

from dataclasses import dataclass
from typing import Optional, Dict, Any, ClassVar, Final

from core.common.errors import ValidationError
from core.common.logging import get_logger

logger = get_logger(__name__)

# Constants for validation
GAME_TYPES: Final[set[str]] = {"Star Rail", "Genshin Impact", "Zenless Zone Zero"}

# Game-specific banner types
BANNER_TYPES_BY_GAME: Final[Dict[str, set[str]]] = {
    "Star Rail": {"Standard", "Limited", "Light Cone"},
    "Genshin Impact": {"Standard", "Limited", "Weapon"},
    "Zenless Zone Zero": {"Standard", "Limited", "W-Engine", "Bangboo"},
}


@dataclass
class BannerConfig:
    """Banner configuration parameters with validation."""

    # Configuration fields
    game_name: str
    banner_type: str
    base_rate: float
    four_star_rate: float
    soft_pity_start_after: int
    hard_pity: int
    rate_increase: float
    guaranteed_rate_up: bool
    rate_up_chance: Optional[float] = None

    # Validation constraints
    _MIN_BASE_RATE: ClassVar[float] = 0.0
    _MAX_BASE_RATE: ClassVar[float] = 1.0
    _MIN_FOUR_STAR_RATE: ClassVar[float] = 0.0
    _MAX_FOUR_STAR_RATE: ClassVar[float] = 1.0
    _MIN_PITY: ClassVar[int] = 1
    _MAX_PITY: ClassVar[int] = 200
    _MIN_RATE_INCREASE: ClassVar[float] = 0.0
    _MAX_RATE_INCREASE: ClassVar[float] = 1.0

    def __post_init__(self) -> None:
        """Validate configuration after initialization.

        Raises:
            ValidationError: If any parameters are invalid
        """
        if not isinstance(self.game_name, str):
            raise ValidationError("game_name must be a string")
        if not isinstance(self.banner_type, str):
            raise ValidationError("banner_type must be a string")
        if not isinstance(self.base_rate, (int, float)):
            raise ValidationError("base_rate must be a number")
        if not isinstance(self.four_star_rate, (int, float)):
            raise ValidationError("four_star_rate must be a number")
        if not isinstance(self.soft_pity_start_after, int):
            raise ValidationError("soft_pity_start_after must be an integer")
        if not isinstance(self.hard_pity, int):
            raise ValidationError("hard_pity must be an integer")
        if not isinstance(self.rate_increase, (int, float)):
            raise ValidationError("rate_increase must be a number")
        if not isinstance(self.guaranteed_rate_up, bool):
            raise ValidationError("guaranteed_rate_up must be a boolean")
        if self.rate_up_chance is not None and not isinstance(
            self.rate_up_chance, (int, float)
        ):
            raise ValidationError("rate_up_chance must be a number or None")

        # Validate game type
        if self.game_name not in GAME_TYPES:
            raise ValidationError(f"Invalid game name. Must be one of: {GAME_TYPES}")

        # Validate banner type for specific game
        valid_banner_types = BANNER_TYPES_BY_GAME.get(self.game_name, set())
        if self.banner_type not in valid_banner_types:
            raise ValidationError(
                f"Invalid banner type for {self.game_name}. Must be one of: {valid_banner_types}"
            )

        # Validate rates
        if not self._MIN_BASE_RATE <= self.base_rate <= self._MAX_BASE_RATE:
            raise ValidationError(
                f"Base rate must be between {self._MIN_BASE_RATE} and {self._MAX_BASE_RATE}"
            )

        if (
            not self._MIN_FOUR_STAR_RATE
            <= self.four_star_rate
            <= self._MAX_FOUR_STAR_RATE
        ):
            raise ValidationError(
                f"Four star rate must be between {self._MIN_FOUR_STAR_RATE} and {self._MAX_FOUR_STAR_RATE}"
            )

        # Validate pity system
        if (
            not self._MIN_PITY
            <= self.soft_pity_start_after
            <= self.hard_pity
            <= self._MAX_PITY
        ):
            raise ValidationError(
                f"Soft pity must be between {self._MIN_PITY} and hard pity, "
                f"hard pity must be between soft pity and {self._MAX_PITY}"
            )

        # Validate rate increase
        if not self._MIN_RATE_INCREASE <= self.rate_increase <= self._MAX_RATE_INCREASE:
            raise ValidationError(
                f"Rate increase must be between {self._MIN_RATE_INCREASE} and {self._MAX_RATE_INCREASE}"
            )

        # Validate rate-up mechanics
        if self.rate_up_chance is not None:
            if not 0 <= self.rate_up_chance <= 1:
                raise ValidationError("Rate up chance must be between 0 and 1")
            if self.rate_up_chance > 0 and not self.guaranteed_rate_up:
                logger.warning("Rate-up chance is set but guaranteed_rate_up is False")
