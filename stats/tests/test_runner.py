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
    # Ensure the first banner succeeds and the second fails
    mock_success_instance = MagicMock()
    mock_success_instance.save_statistics_csv.return_value = {"metric": "path.csv"}
    mock_banner_stats.side_effect = [mock_success_instance, Exception("Test processing error")]
    
    stats_runner.banner_configs = {"star_rail_standard": {}, "genshin_limited": {}}
    stats_runner.process_all_banners()
    
    assert mock_banner_stats.call_count == 2
    # Check that save_statistics_csv was called for the first (successful) banner
    assert mock_success_instance.save_statistics_csv.call_count == 1

def test_process_all_banners_empty_configs(stats_runner, mock_banner_stats, caplog):
    """Test process_all_banners with an empty banner_configs dictionary."""
    stats_runner.banner_configs = {}
    stats_runner.process_all_banners()

    mock_banner_stats.assert_not_called()
    # This test primarily ensures no exceptions are raised.

def test_process_all_banners_first_banner_fails(stats_runner, mock_banner_stats, caplog):
    """Test process_all_banners when the first banner encounters an error."""
    mock_failure_exception = Exception("First banner processing error")
    mock_success_instance = MagicMock()
    mock_success_instance.save_statistics_csv.return_value = {"metric2": "path2.csv"}

    mock_banner_stats.side_effect = [mock_failure_exception, mock_success_instance]
    
    stats_runner.banner_configs = {"star_rail_standard": {}, "genshin_limited": {}}
    stats_runner.process_all_banners()
    
    assert mock_banner_stats.call_count == 2 # Both should be attempted
    mock_banner_stats.assert_any_call(game_type="star", banner_type="rail_standard")
    mock_banner_stats.assert_any_call(game_type="genshin", banner_type="limited")
    
    # Ensure save_statistics_csv was called only for the second (successful) banner
    assert mock_success_instance.save_statistics_csv.call_count == 1

def test_process_all_banners_save_csv_returns_empty(stats_runner, mock_banner_stats, caplog):
    """Test process_all_banners when save_statistics_csv returns an empty dict."""
    mock_instance = mock_banner_stats.return_value
    mock_instance.save_statistics_csv.return_value = {} # Simulate empty file paths

    stats_runner.banner_configs = {"star_rail_standard": {}}
    stats_runner.process_all_banners()

    assert mock_banner_stats.call_count == 1
    mock_banner_stats.assert_called_once_with(game_type="star", banner_type="rail_standard")
    mock_instance.save_statistics_csv.assert_called_once()
    # Ensure no error due to empty dict iteration

@patch("runner.StatsRunner", autospec=True)
@patch("runner.BANNER_CONFIGS", TEST_BANNER_CONFIGS)
def test_main_function(mock_stats_runner_class, caplog):
    """Test the main function orchestrates StatsRunner correctly."""
    mock_runner_instance = mock_stats_runner_class.return_value
    
    main()

    mock_stats_runner_class.assert_called_once_with(TEST_BANNER_CONFIGS)
    mock_runner_instance.process_all_banners.assert_called_once()

