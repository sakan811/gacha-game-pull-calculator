"""Banner configuration module with validation and inheritance support."""

from dataclasses import dataclass
from typing import Optional, ClassVar

from .validation import validate_banner_config


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

    def __post_init__(self):
        """Validate configuration after initialization."""
        validate_banner_config(self)
