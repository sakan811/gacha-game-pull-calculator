import sys
import os
import pytest
from unittest.mock import patch, MagicMock, ANY

# Add the stats directory to sys.path for relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from runner import StatsRunner, main
from core.banner import BannerConfig
from core.banner_stats import BannerStats # Added import
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler


@pytest.fixture
def mock_calculator_class():
    """Fixture to mock ProbabilityCalculator class."""
    with patch("runner.ProbabilityCalculator", autospec=True) as mock_calc_class:
        yield mock_calc_class

@pytest.fixture
def mock_output_handler_class():
    """Fixture to mock CSVOutputHandler class."""
    with patch("runner.CSVOutputHandler", autospec=True) as mock_handler_class:
        yield mock_handler_class

@pytest.fixture
def mock_banner_config_instances():
    """Provides a dictionary of mocked BannerConfig instances."""
    config1 = MagicMock(spec=BannerConfig)
    config1.key = "star_rail_standard"
    config1.game_name = "Star Rail"
    config1.banner_type = "Standard"

    config2 = MagicMock(spec=BannerConfig)
    config2.key = "genshin_limited_character_1"
    config2.game_name = "Genshin Impact"
    config2.banner_type = "Limited"
    
    return {
        config1.key: config1,
        config2.key: config2
    }

@pytest.fixture
def mock_banner_stats(): # This mocks the BannerStats CLASS
    """Fixture to mock the BannerStats class."""
    with patch("runner.BannerStats", autospec=True) as mock_class:
        # This is the instance that will be returned when BannerStats() is called
        mock_instance = mock_class.return_value 
        
        # Set up the .config attribute on the mock_instance because runner.py accesses it
        # e.g., banner_analyzer.config.game_name
        mock_instance.config = MagicMock(spec=BannerConfig)
        mock_instance.config.game_name = "MockedGameForLog"
        mock_instance.config.banner_type = "MockedBannerForLog"

        mock_instance.calculate_probabilities = MagicMock()
        mock_instance.save_results_to_csv.return_value = {
            "metric1": "/fake/path/metric1.csv",
            "metric2": "/fake/path/metric2.csv",
        }
        yield mock_class # yield the mock for the class itself

@pytest.fixture
def stats_runner_with_mocks(mock_banner_config_instances, mock_calculator_class, mock_output_handler_class):
    """Return a StatsRunner instance. Dependencies (ProbCalc, CSVHandler) are mocked at class level."""
    runner = StatsRunner(banner_configs=mock_banner_config_instances)
    return runner


def test_stats_runner_initialization(stats_runner_with_mocks, mock_banner_config_instances, mock_output_handler_class):
    """Test StatsRunner initialization."""
    assert stats_runner_with_mocks.banner_configs == mock_banner_config_instances
    assert isinstance(stats_runner_with_mocks.csv_handler, mock_output_handler_class.return_value.__class__)


def test_process_all_banners_success(stats_runner_with_mocks, mock_banner_stats, caplog, mock_calculator_class):
    """Test process_all_banners successfully processes valid banners."""
    stats_runner_with_mocks.process_all_banners()

    expected_call_count = len(stats_runner_with_mocks.banner_configs)
    assert mock_banner_stats.call_count == expected_call_count
    
    for config_obj in stats_runner_with_mocks.banner_configs.values():
        mock_banner_stats.assert_any_call(
            config=config_obj, 
            calculator=ANY, 
            output_handler=stats_runner_with_mocks.csv_handler
        )

    assert mock_banner_stats.return_value.calculate_probabilities.call_count == expected_call_count
    assert mock_banner_stats.return_value.save_results_to_csv.call_count == expected_call_count
    
    # Check log messages for success. The game_name and banner_type in the log will come from
    # the mock_banner_stats.return_value.config as set in the fixture.
    # This is because the banner_analyzer in runner.py is the mock_banner_stats.return_value.
    expected_log_game_name = mock_banner_stats.return_value.config.game_name
    expected_log_banner_type = mock_banner_stats.return_value.config.banner_type
    expected_log_success = f"Successfully saved stats for {expected_log_game_name} {expected_log_banner_type}:"
    
    # Check if this log message appears for each banner processed
    # The current caplog.messages will contain all logs. We need to ensure this message appears
    # at least once for each banner if the names were dynamic, but since they are fixed from the mock config,
    # we check if the message (with the mocked names) appears `expected_call_count` times.
    # However, the log message itself is generic if multiple banners use the same mocked names.
    # A simpler check is that the log message appears at all, and that the processing loop ran for all items.
    assert any(expected_log_success in message for message in caplog.messages)
    # To be more precise, count occurrences if necessary, but `any` is a good start.
    # Count how many times the success log appears
    success_log_count = sum(1 for message in caplog.messages if expected_log_success in message)
    assert success_log_count == expected_call_count


def test_process_all_banners_invalid_config_value_type(stats_runner_with_mocks, mock_banner_stats, caplog):
    """Test process_all_banners handles invalid config value types (e.g., dict instead of BannerConfig)."""
    stats_runner_with_mocks.banner_configs = {"invalid_data_type_key": {}} 

    stats_runner_with_mocks.process_all_banners() # runner.py will log an error
    
    # The runner.py now explicitly checks for BannerConfig type and logs a TypeError.
    expected_log_message = "Type error or invalid config structure for invalid_data_type_key (UnknownGame - UnknownBanner): Configuration for 'invalid_data_type_key' is not a valid BannerConfig object. Received type: dict"
    assert any(expected_log_message in message for message in caplog.messages)
    mock_banner_stats.assert_not_called()


def test_process_all_banners_processing_error(stats_runner_with_mocks, mock_banner_stats, caplog, mock_banner_config_instances):
    """Test process_all_banners handles exceptions during BannerStats processing."""
    if len(mock_banner_config_instances) < 2:
        pytest.skip("Test requires at least two banner configs.")

    first_config_key = list(mock_banner_config_instances.keys())[0]
    first_config_obj = mock_banner_config_instances[first_config_key]
    second_config_key = list(mock_banner_config_instances.keys())[1]
    second_config_obj = mock_banner_config_instances[second_config_key]
    
    successful_bs_mock = MagicMock(spec=BannerStats)
    successful_bs_mock.config = first_config_obj 
    successful_bs_mock.calculate_probabilities = MagicMock()
    successful_bs_mock.save_results_to_csv.return_value = {"metric": "path.csv"}

    failing_bs_mock = MagicMock(spec=BannerStats)
    failing_bs_mock.config = second_config_obj 
    failing_bs_mock.calculate_probabilities.side_effect = Exception("Test processing error")
    failing_bs_mock.save_results_to_csv = MagicMock()

    mock_banner_stats.side_effect = [successful_bs_mock, failing_bs_mock]

    stats_runner_with_mocks.process_all_banners()

    assert mock_banner_stats.call_count == 2

    successful_bs_mock.calculate_probabilities.assert_called_once()
    successful_bs_mock.save_results_to_csv.assert_called_once()

    failing_bs_mock.calculate_probabilities.assert_called_once()
    failing_bs_mock.save_results_to_csv.assert_not_called()
    
    expected_error_log = f"Unexpected error processing {second_config_key} ({second_config_obj.game_name} - {second_config_obj.banner_type}): Test processing error"
    assert any(expected_error_log in message for message in caplog.messages)
    expected_success_log = f"Successfully saved stats for {first_config_obj.game_name} {first_config_obj.banner_type}:"
    assert any(expected_success_log in message for message in caplog.messages)


def test_process_all_banners_empty_configs(stats_runner_with_mocks, mock_banner_stats, caplog):
    """Test process_all_banners with an empty banner_configs dictionary."""
    stats_runner_with_mocks.banner_configs = {}
    stats_runner_with_mocks.process_all_banners()
    mock_banner_stats.assert_not_called()


def test_process_all_banners_first_banner_fails(stats_runner_with_mocks, mock_banner_stats, caplog, mock_banner_config_instances):
    """Test process_all_banners when the first banner's processing encounters an error."""
    if len(mock_banner_config_instances) < 2:
        pytest.skip("Test requires at least two banner configs.")

    first_config_key = list(mock_banner_config_instances.keys())[0]
    first_config_obj = mock_banner_config_instances[first_config_key]
    second_config_key = list(mock_banner_config_instances.keys())[1]
    second_config_obj = mock_banner_config_instances[second_config_key]

    failing_bs_mock = MagicMock(spec=BannerStats)
    failing_bs_mock.config = first_config_obj
    failing_bs_mock.calculate_probabilities.side_effect = Exception("First banner processing error")
    failing_bs_mock.save_results_to_csv = MagicMock()

    successful_bs_mock = MagicMock(spec=BannerStats)
    successful_bs_mock.config = second_config_obj
    successful_bs_mock.calculate_probabilities = MagicMock()
    successful_bs_mock.save_results_to_csv.return_value = {"metric2": "path2.csv"}
    
    mock_banner_stats.side_effect = [failing_bs_mock, successful_bs_mock]

    stats_runner_with_mocks.process_all_banners()

    assert mock_banner_stats.call_count == 2
    
    failing_bs_mock.calculate_probabilities.assert_called_once()
    failing_bs_mock.save_results_to_csv.assert_not_called()

    successful_bs_mock.calculate_probabilities.assert_called_once()
    successful_bs_mock.save_results_to_csv.assert_called_once()
    
    expected_error_log = f"Unexpected error processing {first_config_key} ({first_config_obj.game_name} - {first_config_obj.banner_type}): First banner processing error"
    assert any(expected_error_log in message for message in caplog.messages)
    expected_success_log = f"Successfully saved stats for {second_config_obj.game_name} {second_config_obj.banner_type}:"
    assert any(expected_success_log in message for message in caplog.messages)


def test_process_all_banners_save_csv_returns_empty(stats_runner_with_mocks, mock_banner_stats, caplog, mock_banner_config_instances):
    """Test process_all_banners when save_results_to_csv returns an empty dict."""
    if not mock_banner_config_instances:
         pytest.skip("Test requires at least one banner config.")
    
    first_config_key = list(mock_banner_config_instances.keys())[0]
    config_obj_for_test = mock_banner_config_instances[first_config_key]
    
    # Configure the mock BannerStats instance that will be returned by the CLASS mock
    # when BannerStats() is called.
    # The mock_banner_stats fixture already sets up mock_banner_stats.return_value.
    # We just need to ensure its save_results_to_csv returns {} for this test.
    # And its .config attribute should reflect the config_obj_for_test for correct logging.
    mock_banner_stats.return_value.config = config_obj_for_test 
    mock_banner_stats.return_value.save_results_to_csv.return_value = {}

    stats_runner_with_mocks.banner_configs = {first_config_key: config_obj_for_test}
    stats_runner_with_mocks.process_all_banners()

    assert mock_banner_stats.call_count == 1
    mock_banner_stats.return_value.calculate_probabilities.assert_called_once()
    mock_banner_stats.return_value.save_results_to_csv.assert_called_once()
    
    expected_log_message = f"Stats processed for {config_obj_for_test.game_name} {config_obj_for_test.banner_type}, but no CSV files were reported as generated."
    assert any(expected_log_message in message for message in caplog.messages)


@patch("runner.StatsRunner", autospec=True)
def test_main_function(mock_stats_runner_class, mock_banner_config_instances, caplog):
    """Test the main function orchestrates StatsRunner correctly."""
    mock_runner_instance = mock_stats_runner_class.return_value

    with patch("runner.BANNER_CONFIGS", mock_banner_config_instances):
        main()

    mock_stats_runner_class.assert_called_once_with(banner_configs=mock_banner_config_instances)
    mock_runner_instance.process_all_banners.assert_called_once()
