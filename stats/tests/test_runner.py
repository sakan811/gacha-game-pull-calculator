import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from core.config.banner_config import BannerConfig
from output.csv_handler import CSVOutputHandler
from core.calculator import ProbabilityCalculator


@pytest.mark.parametrize(
    "game_name,banner_type,expected_file",
    [
        ("Star Rail", "Limited", "star_rail_all_banners.csv"),
        ("Genshin Impact", "Weapon", "genshin_impact_all_banners.csv"),
        ("Zenless Zone Zero", "Bangboo", "zenless_zone_zero_all_banners.csv"),
    ],
)
def test_run_banner_stats_success(game_name, banner_type, expected_file):
    """Test successful execution with different banner configs"""
    config = BannerConfig(
        game_name=game_name,
        banner_type=banner_type,
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.07,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    )

    mock_calculator = Mock(spec=ProbabilityCalculator)
    mock_calculator.calculate_probabilities.return_value = (
        [0.1, 0.2, 0.3],
        [0.05, 0.15, 0.25],
        [0.1, 0.3, 0.5],
    )

    mock_csv = Mock(spec=CSVOutputHandler)

    with (
        patch("runner.BANNER_CONFIGS", {game_name: {banner_type: config}}),
        patch("runner.ProbabilityCalculator", return_value=mock_calculator),
        patch("runner.CSVOutputHandler", return_value=mock_csv),
        patch("runner.format_results"),
        patch("runner.get_headers"),
    ):
        from runner import run_banner_stats

        run_banner_stats()

        mock_calculator.calculate_probabilities.assert_called_once()
        mock_csv.write.assert_called_once()

        # Verify file naming pattern
        args, _ = mock_csv.write.call_args
        assert expected_file in str(Path(args[0]).name).lower()
        assert "csv_output" in str(Path(args[0]).parent).lower()


@pytest.mark.parametrize(
    "error_msg", ["Invalid config", "Calculation error", "Rate out of bounds"]
)
def test_run_banner_stats_error_handling(error_msg: str):
    """Test different error scenarios during calculation"""
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

    mock_csv = Mock(spec=CSVOutputHandler)
    mock_calc = Mock(spec=ProbabilityCalculator)
    mock_calc.calculate_probabilities.side_effect = ValueError(error_msg)

    # We need to patch the logger differently to capture the error
    mock_logger = Mock()

    with (
        patch("runner.BANNER_CONFIGS", {"Star Rail": {"Limited": config}}),
        patch("runner.ProbabilityCalculator", return_value=mock_calc),
        patch("runner.CSVOutputHandler", return_value=mock_csv),
        patch("runner.logger", mock_logger),
    ):
        from runner import run_banner_stats

        run_banner_stats()

        # Verify that error was logged
        error_message = f"Error calculating probabilities for Limited: {error_msg}"
        mock_logger.error.assert_called_once()
        assert error_message in mock_logger.error.call_args[0][0]

        # Verify CSV write is still called (with empty results for the failed banner)
        mock_csv.write.assert_called_once()


def test_run_banner_stats_empty_config():
    """Test handling of empty banner configuration"""
    mock_csv = Mock()

    with (
        patch("runner.BANNER_CONFIGS", {}),
        patch("runner.CSVOutputHandler", return_value=mock_csv),
    ):
        from runner import run_banner_stats

        run_banner_stats()

        # Verify no calculations or writes occurred
        mock_csv.write.assert_not_called()


def test_run_banner_stats_empty_results():
    """Test handling of empty calculation results"""
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

    mock_csv = Mock()
    mock_calc = Mock(spec=ProbabilityCalculator)
    mock_calc.calculate_probabilities.return_value = ([], [], [])

    with (
        patch("runner.BANNER_CONFIGS", {"Star Rail": {"Limited": config}}),
        patch("runner.ProbabilityCalculator", return_value=mock_calc),
        patch("runner.CSVOutputHandler", return_value=mock_csv),
        patch("runner.format_results", return_value=[]),
        patch("runner.get_headers"),
    ):
        from runner import run_banner_stats

        run_banner_stats()

        # Verify CSV was still called with empty results
        mock_csv.write.assert_called_once()
