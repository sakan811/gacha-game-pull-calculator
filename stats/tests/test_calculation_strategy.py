"""Tests for core/calculation/strategy.py"""

import pytest
import numpy as np
from numpy.typing import NDArray
from typing import Dict, Any

from core.calculation.strategy import (
    CalculationResult,
    CalculationStrategy,
    ValidationError,
)


@pytest.fixture
def valid_arrays() -> Dict[str, NDArray[np.float64]]:
    """Create valid probability arrays for testing."""
    return {
        "raw_probabilities": np.array([0.1, 0.2, 0.3], dtype=np.float64),
        "first_5star_prob": np.array([0.1, 0.2, 0.3], dtype=np.float64),
        "cumulative_prob": np.array([0.1, 0.3, 0.5], dtype=np.float64),
    }


@pytest.fixture
def valid_metadata() -> Dict[str, Any]:
    """Create valid metadata for testing."""
    return {
        "base_rate": 0.006,
        "hard_pity": 90,
        "soft_pity_start": 74,
        "rate_increase": 0.06
    }


@pytest.fixture
def valid_calculation_result(valid_arrays, valid_metadata) -> CalculationResult:
    """Create a valid CalculationResult instance."""
    return CalculationResult(
        raw_probabilities=valid_arrays["raw_probabilities"],
        first_5star_prob=valid_arrays["first_5star_prob"],
        cumulative_prob=valid_arrays["cumulative_prob"],
        metadata=valid_metadata
    )


def test_calculation_result_validation(valid_calculation_result):
    """Test CalculationResult validation logic."""
    assert valid_calculation_result.validate() is True


def test_calculation_result_array_type_validation(valid_arrays, valid_metadata):
    """Test array type validation in CalculationResult."""
    arrays = valid_arrays.copy()
    arrays["raw_probabilities"] = [0.1, 0.2, 0.3]  # List instead of ndarray
    
    with pytest.raises(ValidationError, match="All probability arrays must be numpy arrays"):
        CalculationResult(
            raw_probabilities=arrays["raw_probabilities"],
            first_5star_prob=arrays["first_5star_prob"],
            cumulative_prob=arrays["cumulative_prob"],
            metadata=valid_metadata
        ).validate()


def test_calculation_result_empty_array_validation(valid_arrays, valid_metadata):
    """Test empty array validation in CalculationResult."""
    arrays = valid_arrays.copy()
    arrays["raw_probabilities"] = np.array([], dtype=np.float64)
    
    with pytest.raises(ValidationError, match="All probability arrays must be non-empty"):
        CalculationResult(
            raw_probabilities=arrays["raw_probabilities"],
            first_5star_prob=arrays["first_5star_prob"],
            cumulative_prob=arrays["cumulative_prob"],
            metadata=valid_metadata
        ).validate()


@pytest.mark.parametrize("array_key,invalid_value", [
    ("raw_probabilities", 1.2),  # Value > 1
    ("first_5star_prob", -0.2),  # Value < 0
    ("cumulative_prob", 1.5),  # Value > 1
])
def test_calculation_result_probability_bounds(
    array_key: str, 
    invalid_value: float,
    valid_arrays: Dict[str, NDArray[np.float64]], 
    valid_metadata: Dict[str, Any]
):
    """Test probability bounds validation in CalculationResult."""
    arrays = valid_arrays.copy()
    arrays[array_key] = np.array([0.1, invalid_value, 0.3], dtype=np.float64)
    
    with pytest.raises(ValidationError, match="All probabilities must be between 0 and 1"):
        CalculationResult(
            raw_probabilities=arrays["raw_probabilities"],
            first_5star_prob=arrays["first_5star_prob"],
            cumulative_prob=arrays["cumulative_prob"],
            metadata=valid_metadata
        ).validate()


def test_calculation_result_shape_consistency(valid_arrays, valid_metadata):
    """Test that all probability arrays have consistent shapes."""
    arrays = valid_arrays.copy()
    arrays["raw_probabilities"] = np.array([0.1, 0.2], dtype=np.float64)  # Different length
    
    with pytest.raises(ValidationError, match="All probability arrays must have the same shape"):
        CalculationResult(
            raw_probabilities=arrays["raw_probabilities"],
            first_5star_prob=arrays["first_5star_prob"],
            cumulative_prob=arrays["cumulative_prob"],
            metadata=valid_metadata
        ).validate()


def test_calculation_result_array_types(valid_calculation_result):
    """Test array type consistency in calculation results."""
    assert valid_calculation_result.raw_probabilities.dtype == np.float64
    assert valid_calculation_result.first_5star_prob.dtype == np.float64
    assert valid_calculation_result.cumulative_prob.dtype == np.float64


def test_calculation_result_metadata_immutability(valid_calculation_result):
    """Test that metadata cannot be modified after creation."""
    with pytest.raises(AttributeError):
        valid_calculation_result.metadata["new_key"] = "value"


class TestCalculationStrategy(CalculationStrategy):
    """Test implementation of CalculationStrategy."""

    def calculate(self, params: Dict[str, Any]) -> CalculationResult:
        """Calculate test probabilities."""
        return CalculationResult(
            raw_probabilities=np.array([0.1, 0.2, 0.3], dtype=np.float64),
            first_5star_prob=np.array([0.1, 0.2, 0.3], dtype=np.float64),
            cumulative_prob=np.array([0.1, 0.3, 0.5], dtype=np.float64),
            metadata=params,
        )


class InvalidCalculationStrategy(CalculationStrategy):
    """Test implementation that returns invalid results."""

    def calculate(self, params: Dict[str, Any]) -> CalculationResult:
        """Return invalid probability values."""
        return CalculationResult(
            raw_probabilities=np.array([0.1, 1.2, 0.3], dtype=np.float64),  # Invalid > 1
            first_5star_prob=np.array([0.1, 0.2, 0.3], dtype=np.float64),
            cumulative_prob=np.array([0.1, 0.3, 0.5], dtype=np.float64),
            metadata=params,
        )


def test_calculation_strategy():
    """Test CalculationStrategy interface."""
    strategy = TestCalculationStrategy()
    params = {"test": "data"}
    result = strategy.calculate(params)

    assert isinstance(result, CalculationResult)
    assert result.metadata == params
    assert result.validate() is True
    

def test_invalid_calculation_strategy():
    """Test that invalid results are caught by validation."""
    strategy = InvalidCalculationStrategy()
    params = {"test": "data"}
    
    result = strategy.calculate(params)
    with pytest.raises(ValidationError, match="All probabilities must be between 0 and 1"):
        result.validate()


def test_array_shapes():
    """Test that all probability arrays have consistent shapes."""
    strategy = TestCalculationStrategy()
    result = strategy.calculate({})
    
    # All arrays should be the same length
    shape = result.raw_probabilities.shape
    assert result.first_5star_prob.shape == shape
    assert result.cumulative_prob.shape == shape


def test_cumulative_probability_properties():
    """Test properties of cumulative probability array."""
    strategy = TestCalculationStrategy()
    result = strategy.calculate({})
    
    # Cumulative probabilities should be monotonically increasing
    assert np.all(np.diff(result.cumulative_prob) >= 0)
    
    # Should be bounded by 0 and 1
    assert np.all(result.cumulative_prob >= 0)
    assert np.all(result.cumulative_prob <= 1)


def test_array_types():
    """Test array type consistency."""
    strategy = TestCalculationStrategy()
    result = strategy.calculate({})
    
    assert result.raw_probabilities.dtype == np.float64
    assert result.first_5star_prob.dtype == np.float64
    assert result.cumulative_prob.dtype == np.float64
