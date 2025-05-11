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


def test_run_banner_stats_success(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(
        runner,
        "BANNER_CONFIGS",
        {k: {v.banner_type: v} for k, v in mock_banner_configs.items()},
    )
    mock_calc = MagicMock()
    mock_calc_instance = MagicMock()
    mock_calc_instance.calculate_probabilities.return_value = ([0.1], [0.1], [0.1])
    mock_calc.return_value = mock_calc_instance
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    mock_format_results = MagicMock(
        return_value=[["game", "banner", "1", "0.1", "0.1", "0.1"]]
    )
    monkeypatch.setattr(runner, "format_results", mock_format_results)
    monkeypatch.setattr(
        runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"]
    )
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_calc_instance.calculate_probabilities.call_count == 2
    assert mock_csv.write.call_count == 2
    assert mock_format_results.call_count == 2


def test_run_banner_stats_calculation_error(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(
        runner,
        "BANNER_CONFIGS",
        {k: {v.banner_type: v} for k, v in mock_banner_configs.items()},
    )
    mock_calc = MagicMock()
    mock_calc_instance1 = MagicMock()
    mock_calc_instance1.calculate_probabilities.side_effect = Exception("fail")
    mock_calc_instance2 = MagicMock()
    mock_calc_instance2.calculate_probabilities.return_value = ([0.1], [0.1], [0.1])
    mock_calc.side_effect = [mock_calc_instance1, mock_calc_instance2]
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    monkeypatch.setattr(runner, "format_results", MagicMock(return_value=[["row"]]))
    monkeypatch.setattr(
        runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"]
    )
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_csv.write.call_count == 2


def test_run_banner_stats_csv_write_error(monkeypatch, mock_banner_configs):
    monkeypatch.setattr(
        runner,
        "BANNER_CONFIGS",
        {k: {v.banner_type: v} for k, v in mock_banner_configs.items()},
    )
    mock_calc = MagicMock()
    mock_calc_instance = MagicMock()
    mock_calc_instance.calculate_probabilities.return_value = ([0.1], [0.1], [0.1])
    mock_calc.return_value = mock_calc_instance
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    monkeypatch.setattr(runner, "format_results", MagicMock(return_value=[["row"]]))
    monkeypatch.setattr(
        runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"]
    )
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
    monkeypatch.setattr(
        runner,
        "BANNER_CONFIGS",
        {k: {v.banner_type: v} for k, v in mock_banner_configs.items()},
    )
    mock_calc = MagicMock()
    mock_calc_instance = MagicMock()
    mock_calc_instance.calculate_probabilities.return_value = ([], [], [])
    mock_calc.return_value = mock_calc_instance
    monkeypatch.setattr(runner, "ProbabilityCalculator", mock_calc)
    monkeypatch.setattr(runner, "format_results", MagicMock(return_value=[]))
    monkeypatch.setattr(
        runner, "get_headers", lambda: ["h1", "h2", "h3", "h4", "h5", "h6"]
    )
    mock_csv = MagicMock()
    monkeypatch.setattr(runner, "CSVOutputHandler", lambda: mock_csv)
    runner.run_banner_stats()
    assert mock_csv.write.call_count == 2
