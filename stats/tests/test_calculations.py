"""Tests for core calculator and calculation strategy functionality."""

import pytest
import numpy as np
from numpy.typing import NDArray
from typing import Dict, Optional

from core.calculator import ProbabilityCalculator
from core.strategy import (
    CalculationResult,
    CalculationStrategy,
)
from core.banner import BannerConfig
from core.common.errors import ConfigurationError, ValidationError


# Fixtures for shared test data
@pytest.fixture
def valid_arrays() -> Dict[str, NDArray[np.float64]]:
    """Create valid probability arrays for testing."""
    return {
        "raw_probabilities": np.array([0.1, 0.2, 0.3], dtype=np.float64),
        "first_5star_prob": np.array([0.1, 0.2, 0.3], dtype=np.float64),
        "cumulative_prob": np.array([0.1, 0.3, 0.5], dtype=np.float64),
    }


# Test Calculator Implementation
class TestProbabilityCalculator(ProbabilityCalculator):
    """Test implementation of ProbabilityCalculator."""

    def __init__(self, config: Optional[BannerConfig] = None) -> None:
        super().__init__(config)
        self.rolls: NDArray[np.int64] = np.array([], dtype=np.int64)
        self.probabilities: NDArray[np.float64] = np.array([], dtype=np.float64)
        self.p_first_5_star: NDArray[np.float64] = np.array([], dtype=np.float64)
        self.cumulative_prob: NDArray[np.float64] = np.array([], dtype=np.float64)

        if config:
            self.init_with_config()

    def init_with_config(self) -> None:
        """Initialize with current config."""
        if not self.config:
            return
        self.rolls = np.arange(90, dtype=np.int64)
        self.probabilities = np.full(90, 0.006, dtype=np.float64)
        self.p_first_5_star = np.zeros(90, dtype=np.float64)
        self.cumulative_prob = np.zeros(90, dtype=np.float64)


# Calculator Tests
class TestCalculator:
    """Tests for ProbabilityCalculator class."""

    def test_init_without_config(self) -> None:
        """Test initializing calculator without config."""
        calc = TestProbabilityCalculator()
        assert calc.config is None
        assert len(calc.rolls) == 0
        assert len(calc.probabilities) == 0

    def test_init_with_config(self) -> None:
        """Test initializing calculator with valid config."""
        config = BannerConfig(
            game_type="Star Rail",
            banner_type="Limited",
            base_rate=0.006,
            pity_start=74,
            hard_pity=90,
        )
        calc = TestProbabilityCalculator(config=config)
        assert calc.config == config
        assert len(calc.rolls) == 90
        assert len(calc.probabilities) == 90

    def test_validate_config_requirements(self) -> None:
        """Test config validation requirements."""
        with pytest.raises(ConfigurationError):
            TestProbabilityCalculator().validate_config()


# Strategy Tests
class TestCalculationStrategy:
    """Tests for CalculationStrategy class."""

    def test_validate_probability_arrays_with_valid_data(
        self, valid_arrays: Dict[str, NDArray[np.float64]]
    ) -> None:
        """Test array validation with valid data."""
        result = CalculationResult(**valid_arrays)
        CalculationStrategy.validate_probability_arrays(
            raw_probabilities=result.raw_probabilities,
            first_5star_prob=result.first_5star_prob,
            cumulative_prob=result.cumulative_prob,
        )

    def test_validate_probability_arrays_invalid_probabilities(
        self, valid_arrays: Dict[str, NDArray[np.float64]]
    ) -> None:
        """Test array validation with invalid probabilities."""
        invalid_prob = np.array([-0.1, 1.2, 0.3], dtype=np.float64)
        with pytest.raises(ValidationError):
            CalculationStrategy.validate_probability_arrays(
                raw_probabilities=invalid_prob,
                first_5star_prob=valid_arrays["first_5star_prob"],
                cumulative_prob=valid_arrays["cumulative_prob"],
            )

    def test_validate_probability_arrays_mismatched_shapes(
        self, valid_arrays: Dict[str, NDArray[np.float64]]
    ) -> None:
        """Test array validation with mismatched shapes."""
        mismatched_array = np.array([0.1, 0.2], dtype=np.float64)
        with pytest.raises(ValidationError):
            CalculationStrategy.validate_probability_arrays(
                raw_probabilities=valid_arrays["raw_probabilities"],
                first_5star_prob=mismatched_array,
                cumulative_prob=valid_arrays["cumulative_prob"],
            )
