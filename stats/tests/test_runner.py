import sys
import os
import pytest
from unittest.mock import patch, MagicMock, ANY

# Add the stats directory to sys.path for relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from runner import StatsRunner, main
from core.banner import BannerConfig
from core.banner_stats import BannerStats  # Added import


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

    return {config1.key: config1, config2.key: config2}


@pytest.fixture
def mock_banner_stats():  # This mocks the BannerStats CLASS
    """Fixture to mock the BannerStats class."""
    with patch("runner.BannerStats", autospec=True) as mock_class:
        # This is the instance that will be returned when BannerStats() is called
        mock_instance = mock_class.return_value

        # Set up the .config attribute on the mock_instance because runner.py accesses it
        # e.g., banner_analyzer.config.game_name
        mock_instance.config = MagicMock(spec=BannerConfig)
        mock_instance.config.game_name = "MockedGameForLog"
        mock_instance.config.banner_type = "MockedBannerForLog"
        # Add game_name and banner_type directly to the mock for runner.py attribute access
        mock_instance.game_name = mock_instance.config.game_name
        mock_instance.banner_type = mock_instance.config.banner_type

        mock_instance.calculate_probabilities = MagicMock()
        # save_results_to_csv is not used in runner, so do not mock it
        mock_instance.get_banner_rows = MagicMock(return_value=(['header1'], [['row1']]))
        yield mock_class  # yield the mock for the class itself


@pytest.fixture
def stats_runner_with_mocks(
    mock_banner_config_instances, mock_calculator_class, mock_output_handler_class
):
    """Return a StatsRunner instance. Dependencies (ProbCalc, CSVHandler) are mocked at class level."""
    runner = StatsRunner(banner_configs=mock_banner_config_instances)
    return runner


def test_stats_runner_initialization(
    stats_runner_with_mocks, mock_banner_config_instances, mock_output_handler_class
):
    """Test StatsRunner initialization."""
    assert stats_runner_with_mocks.banner_configs == mock_banner_config_instances
    assert isinstance(
        stats_runner_with_mocks.csv_handler,
        mock_output_handler_class.return_value.__class__,
    )


def test_process_all_banners_success(
    stats_runner_with_mocks, mock_banner_stats, caplog, mock_calculator_class
):
    """Test process_all_banners successfully processes valid banners."""
    stats_runner_with_mocks.process_all_banners()

    expected_call_count = len(stats_runner_with_mocks.banner_configs)
    assert mock_banner_stats.call_count == expected_call_count

    for config_obj in stats_runner_with_mocks.banner_configs.values():
        mock_banner_stats.assert_any_call(
            config=config_obj,
            calculator=ANY,
            output_handler=stats_runner_with_mocks.csv_handler,
        )

    assert (
        mock_banner_stats.return_value.calculate_probabilities.call_count
        == expected_call_count
    )
    # Only assert that save_results_to_csv is called if calculate_probabilities does not raise
    # save_results_to_csv is not called by runner, so do not assert on it




def test_process_all_banners_invalid_config_value_type(
    stats_runner_with_mocks, mock_banner_stats, caplog
):
    """Test process_all_banners handles invalid config value types (e.g., dict instead of BannerConfig)."""
    stats_runner_with_mocks.banner_configs = {"invalid_data_type_key": {}}

    stats_runner_with_mocks.process_all_banners()  # runner.py will log an error

    # The runner.py now logs an error with a different prefix, so match the actual log output
    expected_log_message = "Error for invalid_data_type_key (UnknownGame - UnknownBanner): Configuration for 'invalid_data_type_key' is not a valid BannerConfig object. Received type: dict"
    assert any(expected_log_message in message for message in caplog.messages)
    mock_banner_stats.assert_not_called()


def test_process_all_banners_processing_error(
    stats_runner_with_mocks, mock_banner_stats, caplog, mock_banner_config_instances
):
    """Test process_all_banners handles exceptions during BannerStats processing."""
    if len(mock_banner_config_instances) < 2:
        pytest.skip("Test requires at least two banner configs.")

    first_config_key = list(mock_banner_config_instances.keys())[0]
    first_config_obj = mock_banner_config_instances[first_config_key]
    second_config_key = list(mock_banner_config_instances.keys())[1]
    second_config_obj = mock_banner_config_instances[second_config_key]

    successful_bs_mock = MagicMock(spec=BannerStats)
    successful_bs_mock.config = first_config_obj
    successful_bs_mock.game_name = first_config_obj.game_name
    successful_bs_mock.banner_type = first_config_obj.banner_type
    successful_bs_mock.calculate_probabilities = MagicMock()
    successful_bs_mock.get_banner_rows = MagicMock(return_value=(['header1'], [['row1']]))

    failing_bs_mock = MagicMock(spec=BannerStats)
    failing_bs_mock.config = second_config_obj
    failing_bs_mock.game_name = second_config_obj.game_name
    failing_bs_mock.banner_type = second_config_obj.banner_type
    failing_bs_mock.calculate_probabilities = MagicMock()
    failing_bs_mock.calculate_probabilities.side_effect = Exception(
        "Test processing error"
    )
    failing_bs_mock.get_banner_rows = MagicMock(return_value=(['header1'], [['row1']]))

    mock_banner_stats.side_effect = [successful_bs_mock, failing_bs_mock]

    stats_runner_with_mocks.process_all_banners()

    assert mock_banner_stats.call_count == 2

    successful_bs_mock.calculate_probabilities.assert_called_once()
    failing_bs_mock.calculate_probabilities.assert_called_once()




def test_process_all_banners_empty_configs(
    stats_runner_with_mocks, mock_banner_stats, caplog
):
    """Test process_all_banners with an empty banner_configs dictionary."""
    stats_runner_with_mocks.banner_configs = {}
    stats_runner_with_mocks.process_all_banners()
    mock_banner_stats.assert_not_called()


def test_process_all_banners_first_banner_fails(
    stats_runner_with_mocks, mock_banner_stats, caplog, mock_banner_config_instances
):
    """Test process_all_banners when the first banner's processing encounters an error."""
    if len(mock_banner_config_instances) < 2:
        pytest.skip("Test requires at least two banner configs.")

    first_config_key = list(mock_banner_config_instances.keys())[0]
    first_config_obj = mock_banner_config_instances[first_config_key]
    second_config_key = list(mock_banner_config_instances.keys())[1]
    second_config_obj = mock_banner_config_instances[second_config_key]

    failing_bs_mock = MagicMock(spec=BannerStats)
    failing_bs_mock.config = first_config_obj
    failing_bs_mock.game_name = first_config_obj.game_name
    failing_bs_mock.banner_type = first_config_obj.banner_type
    failing_bs_mock.calculate_probabilities = MagicMock()
    failing_bs_mock.calculate_probabilities.side_effect = Exception(
        "First banner processing error"
    )
    failing_bs_mock.get_banner_rows = MagicMock(return_value=(['header1'], [['row1']]))

    successful_bs_mock = MagicMock(spec=BannerStats)
    successful_bs_mock.config = second_config_obj
    successful_bs_mock.game_name = second_config_obj.game_name
    successful_bs_mock.banner_type = second_config_obj.banner_type
    successful_bs_mock.calculate_probabilities = MagicMock()
    successful_bs_mock.get_banner_rows = MagicMock(return_value=(['header1'], [['row1']]))

    mock_banner_stats.side_effect = [failing_bs_mock, successful_bs_mock]

    stats_runner_with_mocks.process_all_banners()

    assert mock_banner_stats.call_count == 2

    failing_bs_mock.calculate_probabilities.assert_called_once()
    successful_bs_mock.calculate_probabilities.assert_called_once()




def test_process_all_banners_save_csv_returns_empty(
    stats_runner_with_mocks, mock_banner_stats, caplog, mock_banner_config_instances
):
    """Test process_all_banners when save_results_to_csv returns an empty dict."""
    if not mock_banner_config_instances:
        pytest.skip("Test requires at least one banner config.")

    first_config_key = list(mock_banner_config_instances.keys())[0]
    config_obj_for_test = mock_banner_config_instances[first_config_key]

    mock_banner_stats.return_value.config = config_obj_for_test

    stats_runner_with_mocks.banner_configs = {first_config_key: config_obj_for_test}
    stats_runner_with_mocks.process_all_banners()

    assert mock_banner_stats.call_count == 1
    mock_banner_stats.return_value.calculate_probabilities.assert_called_once()



@patch("runner.StatsRunner", autospec=True)
def test_main_function(mock_stats_runner_class, mock_banner_config_instances, caplog):
    """Test the main function orchestrates StatsRunner correctly."""
    mock_runner_instance = mock_stats_runner_class.return_value

    with patch("runner.BANNER_CONFIGS", mock_banner_config_instances):
        main()

    mock_stats_runner_class.assert_called_once_with(
        banner_configs=mock_banner_config_instances
    )
    mock_runner_instance.process_all_banners.assert_called_once()
