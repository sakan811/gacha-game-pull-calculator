# Tests for core/banner.py
from core.banner import BannerConfig


# Test BannerConfig
def test_banner_config_creation():
    """Test creation of BannerConfig objects."""
    config = BannerConfig(
        game_name="Test Game",  # Added
        banner_type="Test Banner",  # Added
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    )
    assert config.game_name == "Test Game"  # Added
    assert config.banner_type == "Test Banner"  # Added
    assert config.base_rate == 0.006
    assert config.four_star_rate == 0.051
    assert config.soft_pity_start_after == 73
    assert config.hard_pity == 90
    assert config.rate_increase == 0.06
    assert config.guaranteed_rate_up is True
    assert config.rate_up_chance == 0.5


def test_banner_config_optional_rate_up_chance():
    """Test BannerConfig with optional rate_up_chance."""
    config = BannerConfig(
        game_name="Test Game 2",  # Added
        banner_type="Another Banner",  # Added
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=False,
    )
    assert config.rate_up_chance is None
