"""Banner configuration module with validation and inheritance support."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, ClassVar


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

    # Cached properties
    _validated: bool = field(init=False, default=False, repr=False)

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self.validate()
        self._validated = True

    def validate(self) -> None:
        """Validate banner configuration parameters.

        Raises:
            ValueError: If any parameter is invalid.
        """
        if not self._MIN_BASE_RATE <= self.base_rate <= self._MAX_BASE_RATE:
            raise ValueError(
                f"Base rate must be between {self._MIN_BASE_RATE} and {self._MAX_BASE_RATE}"
            )

        if (
            not self._MIN_FOUR_STAR_RATE
            <= self.four_star_rate
            <= self._MAX_FOUR_STAR_RATE
        ):
            raise ValueError(
                f"Four star rate must be between {self._MIN_FOUR_STAR_RATE} and {self._MAX_FOUR_STAR_RATE}"
            )

        if (
            not self._MIN_PITY
            <= self.soft_pity_start_after
            <= self.hard_pity
            <= self._MAX_PITY
        ):
            raise ValueError(
                f"Soft pity must be between {self._MIN_PITY} and hard pity, hard pity must be between soft pity and {self._MAX_PITY}"
            )

        if self.rate_up_chance is not None and not 0 <= self.rate_up_chance <= 1:
            raise ValueError("Rate up chance must be between 0 and 1")

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization."""
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
        """Create config from dictionary for deserialization."""
        return cls(**data)

    def create_variant(self, **updates: Any) -> "BannerConfig":
        """Create a new banner config inheriting from this one with updates."""
        data = self.to_dict()
        data.update(updates)
        return self.from_dict(data)
