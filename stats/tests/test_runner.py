import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add the stats directory to sys.path for relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from runner import StatsRunner, main
from core.banner_config import BANNER_CONFIGS

TEST_BANNER_CONFIGS = {
    "star_rail_standard": {},
    "genshin_limited": {},
    "invalidkey": {}  # For testing error handling
}

@pytest.fixture
def mock_banner_stats():
    """Fixture to mock the BannerStats class."""
    with patch("runner.BannerStats", autospec=True) as mock:
        mock_instance = mock.return_value
        mock_instance.save_statistics_csv.return_value = {
            "metric1": "/fake/path/metric1.csv",
            "metric2": "/fake/path/metric2.csv"
        }
        yield mock

@pytest.fixture
def stats_runner():
    """Return a StatsRunner instance with mocked banner_configs."""
    return StatsRunner(banner_configs=TEST_BANNER_CONFIGS)

def test_stats_runner_initialization(stats_runner):
    """Test StatsRunner initialization."""
    assert stats_runner.banner_configs == TEST_BANNER_CONFIGS

def test_process_all_banners_success(stats_runner, mock_banner_stats, caplog):
    """Test process_all_banners successfully processes valid banners."""
    stats_runner.banner_configs = {
        "star_rail_standard": {},
        "genshin_limited": {}
    }
    stats_runner.process_all_banners()
    
    assert mock_banner_stats.call_count == 2
    mock_banner_stats.assert_any_call(game_type="star", banner_type="rail_standard")
    mock_banner_stats.assert_any_call(game_type="genshin", banner_type="limited")

    for call_arg in mock_banner_stats.return_value.save_statistics_csv.call_args_list:
        assert call_arg == ()
    assert mock_banner_stats.return_value.save_statistics_csv.call_count == 2

def test_process_all_banners_invalid_key_format(stats_runner, mock_banner_stats, caplog):
    """Test process_all_banners handles invalid config key formats."""
    stats_runner.banner_configs = {"invalidkeyformat": {}}
    stats_runner.process_all_banners()

    mock_banner_stats.assert_not_called()
    assert "Skipping invalid config key format: invalidkeyformat" in caplog.text

def test_process_all_banners_processing_error(stats_runner, mock_banner_stats, caplog):
    """Test process_all_banners handles exceptions during BannerStats processing."""
    mock_banner_stats.side_effect = [MagicMock(save_statistics_csv=MagicMock(return_value={"metric": "path.csv"})), Exception("Test processing error")]
    
    stats_runner.banner_configs = {"star_rail_standard": {}, "genshin_limited": {}}
    stats_runner.process_all_banners()
    
    assert mock_banner_stats.call_count == 2

@patch("runner.StatsRunner", autospec=True)
@patch("runner.BANNER_CONFIGS", TEST_BANNER_CONFIGS)
def test_main_function(mock_stats_runner_class, caplog):
    """Test the main function orchestrates StatsRunner correctly."""
    mock_runner_instance = mock_stats_runner_class.return_value
    
    main()

    mock_stats_runner_class.assert_called_once_with(TEST_BANNER_CONFIGS)
    mock_runner_instance.process_all_banners.assert_called_once()

