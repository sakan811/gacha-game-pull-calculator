"""Banner configuration module with validation and inheritance support.

This module provides the BannerConfig class for defining and validating banner parameters
across different games and banner types. It supports inheritance and serialization.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, ClassVar, Final

from core.common.errors import ValidationError, ConfigurationError
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


@dataclass(frozen=True)
class BannerConfig:
    """Banner configuration parameters with validation.

    This class represents the configuration for a gacha banner, including rates,
    pity systems, and rate-up mechanics. It validates all parameters on initialization
    and provides methods for serialization and creating variants.

    Attributes:
        game_name: Name of the game (Star Rail, Genshin Impact, etc.)
        banner_type: Type of banner (Standard, Limited, etc.)
        base_rate: Base probability of getting a 5-star
        four_star_rate: Base probability of getting a 4-star
        soft_pity_start_after: Roll number when soft pity begins
        hard_pity: Roll number when 5-star is guaranteed
        rate_increase: Probability increase per roll during soft pity
        guaranteed_rate_up: Whether rate-up is guaranteed after non-rate-up
        rate_up_chance: Probability of getting rate-up character when getting 5-star
    """

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

    # Cached properties
    _validated: bool = field(init=False, default=False, repr=False)

    def __post_init__(self) -> None:
        """Validate configuration after initialization.

        Raises:
            ValidationError: If any parameter is invalid
        """
        try:
            self.validate()
            object.__setattr__(self, "_validated", True)
        except Exception as e:
            logger.error(f"Banner configuration validation failed: {str(e)}")
            raise ValidationError(f"Invalid banner configuration: {str(e)}")

    def validate(self) -> None:
        """Validate banner configuration parameters.

        Performs comprehensive validation of all banner parameters including:
        - Game and banner type validation
        - Rate bounds checking
        - Pity system consistency
        - Rate-up mechanics validation

        Raises:
            ValidationError: If any parameter is invalid
        """        
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization.

        Returns:
            Dictionary containing all configuration parameters
        """
        return {
            "game_name": self.game_name,
            "banner_type": self.banner_type,
            "base_rate": self.base_rate,
            "four_star_rate": self.four_star_rate,
            "soft_pity_start_after": self.soft_pity_start_after,
            "hard_pity": self.hard_pity,
            "rate_increase": self.rate_increase,
            "guaranteed_rate_up": self.guaranteed_rate_up,
            "rate_up_chance": self.rate_up_chance,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BannerConfig":
        """Create config from dictionary for deserialization.

        Args:
            data: Dictionary containing configuration parameters

        Returns:
            New BannerConfig instance

        Raises:
            ConfigurationError: If the data is invalid or missing required fields
        """
        required_fields = {
            "game_name",
            "banner_type",
            "base_rate",
            "four_star_rate",
            "soft_pity_start_after",
            "hard_pity",
            "rate_increase",
            "guaranteed_rate_up",
        }

        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise ConfigurationError(f"Missing required fields: {missing_fields}")

        try:
            return cls(**data)
        except Exception as e:
            logger.error(f"Failed to create banner config from dict: {str(e)}")
            raise ConfigurationError(f"Invalid configuration data: {str(e)}")

    def create_variant(self, **updates: Any) -> "BannerConfig":
        """Create a new banner config inheriting from this one with updates.

        This method allows creating variations of existing configs by
        overriding specific parameters while inheriting the rest.

        Args:
            **updates: Keyword arguments of parameters to update

        Returns:
            New BannerConfig instance with updated parameters

        Raises:
            ConfigurationError: If the resulting configuration would be invalid
        """
        try:
            data = self.to_dict()
            data.update(updates)
            return self.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to create banner config variant: {str(e)}")
            raise ConfigurationError(f"Invalid variant configuration: {str(e)}")
