"""Pytest tests for BannerStatisticsRunner."""

import os
import tempfile
from typing import List

import pytest

from core.config.banner_config import BannerConfig, BANNER_CONFIGS, GAME_TYPES
from output.csv_handler import CSVOutputHandler
from runner import BannerStatisticsRunner


class MockCSVOutputHandler(CSVOutputHandler):
    """Mock CSV output handler for testing that inherits from CSVOutputHandler."""

    def __init__(self, encoding: str = "utf-8"):
        """
        Initialize mock output handler.

        Args:
            encoding: File encoding (defaults to utf-8)
        """
        super().__init__(encoding)
        self.written_files: List[str] = []
        self.headers: List[List[str]] = []
        self.rows: List[List[List[str]]] = []

    def write(
        self,
        filename: str,
        header: List[str],
        rows: List[List[str]],
    ) -> None:
        """
        Mock write method to capture output details.

        Args:
            filename: Path to write CSV
            header: CSV headers
            rows: CSV data rows
        """
        # First, call the parent method to maintain original validation
        super().write(filename, header, rows)

        # Then capture the details for testing
        self.written_files.append(filename)
        self.headers.append(header)
        self.rows.append(rows)


class MockLogger:
    """Mock logger for testing."""

    def __init__(self):
        self.info_logs: List[str] = []
        self.error_logs: List[str] = []

    def info(self, message: str):
        """Capture info logs."""
        self.info_logs.append(message)

    def error(self, message: str, exc_info: bool = False):
        """Capture error logs."""
        self.error_logs.append(message)


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(original_cwd)


@pytest.fixture
def mock_output_handler():
    """Create a mock CSV output handler."""
    return MockCSVOutputHandler()


@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    return MockLogger()


def test_default_initialization():
    """Test default initialization with no custom dependencies."""
    runner = BannerStatisticsRunner()

    # Verify default dependencies
    assert runner.banner_configs == BANNER_CONFIGS
    assert isinstance(runner.output_handler, CSVOutputHandler)
    assert runner.logger is not None


def test_custom_dependencies(mock_output_handler, mock_logger):
    """Test initialization with custom dependencies."""
    # Use a valid game name from GAME_TYPES
    valid_game_name = list(GAME_TYPES)[0]  # Pick the first game type

    # Custom mock dependencies
    custom_configs = {
        valid_game_name: {
            "test_banner": BannerConfig(
                game_name=valid_game_name,
                banner_type="Standard",  # Use a valid banner type
                base_rate=0.01,
                four_star_rate=0.051,
                soft_pity_start_after=70,
                hard_pity=90,
                rate_increase=0.06,
                guaranteed_rate_up=False,
            )
        }
    }

    runner = BannerStatisticsRunner(
        banner_configs=custom_configs,
        output_handler=mock_output_handler,
        logger=mock_logger,
    )

    # Verify custom dependencies
    assert runner.banner_configs == custom_configs
    assert runner.output_handler == mock_output_handler
    assert runner.logger == mock_logger


def test_run_method(mock_output_handler, mock_logger):
    """Test full run method with mock dependencies."""
    runner = BannerStatisticsRunner(
        output_handler=mock_output_handler, logger=mock_logger
    )

    # Run the statistics calculation
    runner.run()

    # Verify output
    assert len(mock_output_handler.written_files) > 0

    # Check logs
    assert any(
        "Starting banner statistics calculation" in log for log in mock_logger.info_logs
    )
    assert any(
        "Banner statistics calculation completed" in log
        for log in mock_logger.info_logs
    )


def test_output_directory_creation(temp_output_dir):
    """Test that output directory is created."""
    runner = BannerStatisticsRunner()
    runner.run()

    # Verify CSV output directory exists
    assert os.path.exists("csv_output")
    assert os.path.isdir("csv_output")


def test_error_handling(mock_output_handler, mock_logger, monkeypatch):
    """Test error handling during calculation."""

    # Simulate a calculation error
    def mock_calculate_probabilities(*args, **kwargs):
        raise Exception("Test calculation error")

    # Patch the calculate_probabilities method
    monkeypatch.setattr(
        "core.calculator.ProbabilityCalculator.calculate_probabilities",
        mock_calculate_probabilities,
    )

    runner = BannerStatisticsRunner(
        output_handler=mock_output_handler, logger=mock_logger
    )

    # Run should not raise an exception
    runner.run()

    # Verify error was logged
    assert any(
        "Error calculating probabilities" in log for log in mock_logger.error_logs
    )
