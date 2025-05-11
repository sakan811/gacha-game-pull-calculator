"""Banner configuration validation module."""
from typing import Any

from ..common.errors import ValidationError
from ..common.logging import get_logger

logger = get_logger(__name__)


def validate_banner_config(config: Any) -> None:
    """Validate banner configuration parameters.
    
    Args:
        config: BannerConfig instance to validate
        
    Raises:
        ValidationError: If any configuration parameter is invalid
    """
    _validate_rates(config)
    _validate_pity_values(config)
    _validate_rate_up(config)
    logger.debug(f"Banner config validation passed for {config.game_name} - {config.banner_type}")


def _validate_rates(config: Any) -> None:
    """Validate rate-related parameters."""
    if not config._MIN_BASE_RATE <= config.base_rate <= config._MAX_BASE_RATE:
        raise ValidationError(
            f"Base rate must be between {config._MIN_BASE_RATE} and {config._MAX_BASE_RATE}"
        )
    
    if not config._MIN_FOUR_STAR_RATE <= config.four_star_rate <= config._MAX_FOUR_STAR_RATE:
        raise ValidationError(
            f"Four star rate must be between {config._MIN_FOUR_STAR_RATE} and {config._MAX_FOUR_STAR_RATE}"
        )


def _validate_pity_values(config: Any) -> None:
    """Validate pity-related parameters."""
    if not config._MIN_PITY <= config.soft_pity_start_after <= config._MAX_PITY:
        raise ValidationError(
            f"Soft pity must be between {config._MIN_PITY} and {config._MAX_PITY}"
        )
    
    if not config._MIN_PITY <= config.hard_pity <= config._MAX_PITY:
        raise ValidationError(
            f"Hard pity must be between {config._MIN_PITY} and {config._MAX_PITY}"
        )
    
    if config.soft_pity_start_after >= config.hard_pity:
        raise ValidationError("Soft pity must be less than hard pity")
