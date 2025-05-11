
import pytest
from unittest.mock import MagicMock
import runner



@pytest.fixture
def mock_banner_configs():
    config1 = MagicMock()
    config1.game_name = "Star Rail"
    config1.banner_type = "Standard"
    config2 = MagicMock()
    config2.game_name = "Genshin Impact"
    config2.banner_type = "Limited"
    return {"star_rail_standard": config1, "genshin_limited": config2}




@pytest.fixture
def stats_runner_with_mocks(
    mock_banner_config_instances, mock_calculator_class, mock_output_handler_class
):
    """Return a StatsRunner instance. Dependencies (ProbCalc, CSVHandler) are mocked at class level."""
    runner = StatsRunner()
    runner.banner_configs = mock_banner_config_instances
    return runner
    return runner



def test_run_banner_stats_success(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(runner, "BANNER_CONFIGS", {k: {v.banner_type: v} for k, v in mock_banner_configs.items()})
    mock_calc = MagicMock()
    mock_calc_instance = MagicMock()
    mock_calc_instance.calculate_probabilities.return_value = ([0.1], [0.1], [0.1])
    mock_calc.return_value = mock_calc_instance
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    mock_format_results = MagicMock(return_value=[["game", "banner", "1", "0.1", "0.1", "0.1"]])
    monkeypatch.setattr(runner, "format_results", mock_format_results)
    monkeypatch.setattr(runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"])
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_calc_instance.calculate_probabilities.call_count == 2
    assert mock_csv.write.call_count == 2
    assert mock_format_results.call_count == 2

def test_run_banner_stats_calculation_error(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(runner, "BANNER_CONFIGS", {k: {v.banner_type: v} for k, v in mock_banner_configs.items()})
    mock_calc = MagicMock()
    mock_calc_instance1 = MagicMock()
    mock_calc_instance1.calculate_probabilities.side_effect = Exception("fail")
    mock_calc_instance2 = MagicMock()
    mock_calc_instance2.calculate_probabilities.return_value = ([0.1], [0.1], [0.1])
    mock_calc.side_effect = [mock_calc_instance1, mock_calc_instance2]
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    monkeypatch.setattr(runner, "format_results", MagicMock(return_value=[["row"]]))
    monkeypatch.setattr(runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"])
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_csv.write.call_count == 2

def test_run_banner_stats_csv_write_error(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(runner, "BANNER_CONFIGS", {k: {v.banner_type: v} for k, v in mock_banner_configs.items()})
    mock_calc = MagicMock()
    mock_calc_instance = MagicMock()
    mock_calc_instance.calculate_probabilities.return_value = ([0.1], [0.1], [0.1])
    mock_calc.return_value = mock_calc_instance
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    monkeypatch.setattr(runner, "format_results", MagicMock(return_value=[["row"]]))
    monkeypatch.setattr(runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"])
    mock_csv = MagicMock()
    mock_csv.write.side_effect = Exception("csv fail")
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_csv.write.call_count == 2

def test_run_banner_stats_empty_configs(monkeypatch):
    monkeypatch.setattr(runner, "BANNER_CONFIGS", {})
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_csv.write.call_count == 0

def test_run_banner_stats_empty_results(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(runner, "BANNER_CONFIGS", {k: {v.banner_type: v} for k, v in mock_banner_configs.items()})
    mock_calc = MagicMock()
    mock_calc_instance = MagicMock()
    mock_calc_instance.calculate_probabilities.return_value = ([], [], [])
    mock_calc.return_value = mock_calc_instance
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    monkeypatch.setattr(runner, "format_results", MagicMock(return_value=[]))
    monkeypatch.setattr(runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"])
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_csv.write.call_count == 2


def test_process_all_banners_success(
    stats_runner_with_mocks, mock_banner_stats, caplog, mock_calculator_class
):
    """Test process_all_banners successfully processes valid banners."""
    stats_runner_with_mocks.process_all_banners()

    expected_call_count = len(stats_runner_with_mocks.banner_configs)
    assert mock_banner_stats.call_count == expected_call_count

    for config_obj in stats_runner_with_mocks.banner_configs.values():
        # Only check if config has required attributes
        if hasattr(config_obj, "game_name") and hasattr(config_obj, "banner_type"):
            mock_banner_stats.assert_any_call(
                config=config_obj,
                calculator=ANY,
                output_handler=stats_runner_with_mocks.csv_handler,
            )

    assert (
        mock_banner_stats.return_value.calculate_probabilities.call_count
        == expected_call_count
    )


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

    successful_bs_mock = MagicMock()
    successful_bs_mock.config = first_config_obj
    successful_bs_mock.game_name = first_config_obj.game_name
    successful_bs_mock.banner_type = first_config_obj.banner_type
    successful_bs_mock.calculate_probabilities = MagicMock()
    successful_bs_mock.get_banner_rows = MagicMock(
        return_value=(["header1"], [["row1"]])
    )

    failing_bs_mock = MagicMock()
    failing_bs_mock.config = second_config_obj
    failing_bs_mock.game_name = second_config_obj.game_name
    failing_bs_mock.banner_type = second_config_obj.banner_type
    failing_bs_mock.calculate_probabilities = MagicMock()
    failing_bs_mock.calculate_probabilities.side_effect = Exception(
        "Test processing error"
    )
    failing_bs_mock.get_banner_rows = MagicMock(return_value=(["header1"], [["row1"]]))

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

    failing_bs_mock = MagicMock()
    failing_bs_mock.config = first_config_obj
    failing_bs_mock.game_name = first_config_obj.game_name
    failing_bs_mock.banner_type = first_config_obj.banner_type
    failing_bs_mock.calculate_probabilities = MagicMock()
    failing_bs_mock.calculate_probabilities.side_effect = Exception(
        "First banner processing error"
    )
    failing_bs_mock.get_banner_rows = MagicMock(return_value=(["header1"], [["row1"]]))

    successful_bs_mock = MagicMock()
    successful_bs_mock.config = second_config_obj
    successful_bs_mock.game_name = second_config_obj.game_name
    successful_bs_mock.banner_type = second_config_obj.banner_type
    successful_bs_mock.calculate_probabilities = MagicMock()
    successful_bs_mock.get_banner_rows = MagicMock(
        return_value=(["header1"], [["row1"]])
    )

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
