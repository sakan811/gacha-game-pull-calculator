# Tests for core/config/banner.py
import pytest
from core.common.errors import ValidationError
from stats.core.config.banner_config import BannerConfig


def test_banner_config_creation_star_rail():
    """Test creating valid BannerConfig for Star Rail."""
    config = BannerConfig(
        game_name="Star Rail",
        banner_type="Limited",
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    )
    assert config.game_name == "Star Rail"
    assert config.banner_type == "Limited"
    assert config.base_rate == 0.006
    assert config.four_star_rate == 0.051
    assert config.soft_pity_start_after == 73
    assert config.hard_pity == 90
    assert config.rate_increase == 0.07
    assert config.guaranteed_rate_up is True
    assert config.rate_up_chance == 0.5


def test_banner_config_validation_game_type():
    """Test validation of game type."""
    with pytest.raises(ValidationError, match="Invalid game name"):
        BannerConfig(
            game_name="Invalid Game",
            banner_type="Standard",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=False,
        )


def test_banner_config_validation_banner_type():
    """Test validation of banner type for specific game."""
    with pytest.raises(ValidationError, match="Invalid banner type"):
        BannerConfig(
            game_name="Star Rail",
            banner_type="Invalid Banner",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=False,
        )


def test_banner_config_optional_rate_up_chance_star_rail():
    """Test BannerConfig with optional rate_up_chance for Star Rail Standard banner."""
    config = BannerConfig(
        game_name="Star Rail",
        banner_type="Standard",
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
    )
    assert config.rate_up_chance is None


def test_banner_config_validation_pity_range():
    """Test validation of pity system ranges."""
    with pytest.raises(ValidationError, match="Invalid pity values"):
        BannerConfig(
            game_name="Star Rail",
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=0,  # Invalid: too low
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
        )

    with pytest.raises(ValidationError, match="Invalid pity values"):
        BannerConfig(
            game_name="Star Rail",
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=91,  # Invalid: higher than hard pity
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
        )


def test_banner_config_validation_rates():
    """Test validation of rate values."""
    with pytest.raises(ValidationError, match="Base rate must be between"):
        BannerConfig(
            game_name="Star Rail",
            banner_type="Limited",
            base_rate=1.5,  # Invalid: > 1.0
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
        )

    with pytest.raises(ValidationError, match="Rate up chance must be between"):
        BannerConfig(
            game_name="Star Rail",
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
            rate_up_chance=2.0,  # Invalid: > 1.0
        )


def test_banner_config_genshin_impact():
    """Test BannerConfig creation for Genshin Impact."""
    config = BannerConfig(
        game_name="Genshin Impact",
        banner_type="Weapon",
        base_rate=0.007,
        four_star_rate=0.066,
        soft_pity_start_after=62,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.75,
    )
    assert config.game_name == "Genshin Impact"
    assert config.banner_type == "Weapon"
    assert config.rate_up_chance == 0.75


def test_banner_config_zenless():
    """Test BannerConfig creation for Zenless Zone Zero."""
    config = BannerConfig(
        game_name="Zenless Zone Zero",
        banner_type="Bangboo",
        base_rate=0.01,
        four_star_rate=0.051,
        soft_pity_start_after=64,
        hard_pity=80,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=1.0,
    )
    assert config.game_name == "Zenless Zone Zero"
    assert config.banner_type == "Bangboo"
    assert config.rate_up_chance == 1.0


def test_banner_config_warning_rate_up_without_guarantee():
    """Test warning when rate up is set without guarantee."""
    # This should log a warning but not raise an error
    BannerConfig(
        game_name="Star Rail",
        banner_type="Standard",
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=False,
        rate_up_chance=0.5,  # Setting rate_up_chance without guaranteed_rate_up
    )


def test_banner_config_type_validation():
    """Test type validation of banner config parameters."""
    with pytest.raises(ValidationError):
        BannerConfig(
            game_name=123,  # type: ignore
            banner_type="Limited",
            base_rate=0.006,
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
        )

    with pytest.raises(ValidationError):
        BannerConfig(
            game_name="Star Rail",
            banner_type="Limited",
            base_rate="0.006",  # type: ignore
            four_star_rate=0.051,
            soft_pity_start_after=73,
            hard_pity=90,
            rate_increase=0.07,
            guaranteed_rate_up=True,
        )
