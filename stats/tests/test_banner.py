# Tests for core/banner.py
import pytest
from core.banner import BannerConfig, BaseBanner

# Test BannerConfig
def test_banner_config_creation():
    """Test creation of BannerConfig objects."""
    config = BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=True,
        rate_up_chance=0.5
    )
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
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=False
    )
    assert config.rate_up_chance is None

# Test BaseBanner
@pytest.fixture
def sample_banner_config():
    """Return a sample BannerConfig for testing."""
    return BannerConfig(
        base_rate=0.01,
        four_star_rate=0.1,
        soft_pity_start_after=70,
        hard_pity=90,
        rate_increase=0.05,
        guaranteed_rate_up=True,
        rate_up_chance=0.75
    )

@pytest.fixture
def base_banner(sample_banner_config):
    """Return a BaseBanner instance with sample config."""
    return BaseBanner(config=sample_banner_config)

def test_base_banner_initialization(base_banner, sample_banner_config):
    """Test BaseBanner initialization."""
    assert base_banner.config == sample_banner_config

def test_base_banner_get_base_rate(base_banner, sample_banner_config):
    """Test get_base_rate method."""
    assert base_banner.get_base_rate() == sample_banner_config.base_rate

def test_base_banner_get_hard_pity(base_banner, sample_banner_config):
    """Test get_hard_pity method."""
    assert base_banner.get_hard_pity() == sample_banner_config.hard_pity

def test_base_banner_get_soft_pity_start(base_banner, sample_banner_config):
    """Test get_soft_pity_start method."""
    assert base_banner.get_soft_pity_start() == sample_banner_config.soft_pity_start_after
