# Tests for core/calculation/calculator.py
import pytest
import numpy as np
from numpy.typing import NDArray
from core.calculation import ProbabilityCalculator
from core.config import BannerConfig
from typing import Optional
from core.common.errors import ConfigurationError


class TestProbabilityCalculator(ProbabilityCalculator):
    """Test implementation of ProbabilityCalculator."""

    def __init__(self, config: Optional[BannerConfig] = None) -> None:
        super().__init__(config)
        self.rolls: NDArray[np.int64] = np.array([], dtype=np.int64)
        self.probabilities: NDArray[np.float64] = np.array([], dtype=np.float64)
        self.p_first_5_star: NDArray[np.float64] = np.array([], dtype=np.float64)
        self.cumulative_prob: NDArray[np.float64] = np.array([], dtype=np.float64)
        
        if config:
            try:
                self._initialize_calculations()
            except Exception as e:
                raise ConfigurationError(f"Invalid banner configuration: {str(e)}")


class TestProbabilityCalculator(ProbabilityCalculator):
    """Test implementation of ProbabilityCalculator."""

    def _calculate_raw_probabilities(self) -> NDArray[np.float64]:
        if not self.config:
            raise ValueError("Config must be set to calculate raw probabilities.")
            
        rolls = np.arange(1, self.config.hard_pity + 1)
        probs = np.full_like(rolls, self.config.base_rate, dtype=np.float64)
        
        soft_mask = (rolls >= self.config.soft_pity_start_after + 1) & (rolls < self.config.hard_pity)
        probs[soft_mask] = np.minimum(
            1.0, 
            self.config.base_rate + (rolls[soft_mask] - self.config.soft_pity_start_after) * self.config.rate_increase
        )
        probs[-1] = 1.0  # Hard pity
        return probs

    def _calculate_first_5star_prob_from_raw(
        self, raw_probabilities: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        result = np.zeros_like(raw_probabilities)
        cumulative_fail = 1.0
        for i, prob in enumerate(raw_probabilities):
            prob_here = cumulative_fail * prob
            cumulative_fail *= (1 - prob)
            result[i] = prob_here
        return result

    def _calculate_cumulative_prob_from_raw(
        self, raw_probabilities: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        result = np.zeros_like(raw_probabilities)
        cumulative_fail = 1.0
        for i, prob in enumerate(raw_probabilities):
            cumulative_fail *= (1 - prob)
            result[i] = 1 - cumulative_fail
        return result


@pytest.fixture
def sample_banner_config_for_calc():
    """Return a sample BannerConfig for calculator testing."""
    return BannerConfig(
        game_name="TestGame",  # Added
        banner_type="TestBanner",  # Added
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=True,
        rate_up_chance=0.5,
    )


@pytest.fixture
def probability_calculator(sample_banner_config_for_calc):
    """Return a TestProbabilityCalculator instance, initialized with config."""
    calc = TestProbabilityCalculator(config=sample_banner_config_for_calc)
    return calc


def test_calculator_initialization_with_config(
    probability_calculator, sample_banner_config_for_calc
):
    """Test ProbabilityCalculator initialization with a config."""
    assert probability_calculator.config == sample_banner_config_for_calc
    
    # Check array initializations
    assert probability_calculator.rolls.dtype == np.int64
    assert probability_calculator.probabilities.dtype == np.float64
    assert probability_calculator.p_first_5_star.dtype == np.float64
    assert probability_calculator.cumulative_prob.dtype == np.float64
    
    # Check array lengths
    assert len(probability_calculator.rolls) == sample_banner_config_for_calc.hard_pity
    assert len(probability_calculator.probabilities) == sample_banner_config_for_calc.hard_pity
    assert len(probability_calculator.p_first_5_star) == sample_banner_config_for_calc.hard_pity
    assert len(probability_calculator.cumulative_prob) == sample_banner_config_for_calc.hard_pity
    
    # Check array content
    assert np.all(probability_calculator.probabilities >= 0) and np.all(probability_calculator.probabilities <= 1)
    assert np.all(probability_calculator.p_first_5_star >= 0) and np.all(probability_calculator.p_first_5_star <= 1)
    assert np.all(probability_calculator.cumulative_prob >= 0) and np.all(probability_calculator.cumulative_prob <= 1)


def test_calculator_initialization_without_config():
    """Test ProbabilityCalculator initialization without a config."""
    calc = TestProbabilityCalculator()
    assert calc.config is None
    assert len(calc.rolls) == 0
    assert len(calc.probabilities) == 0
    assert len(calc.p_first_5_star) == 0
    assert len(calc.cumulative_prob) == 0


def test_calculate_probabilities_before_config_raises_error():
    """Test that _calculate_raw_probabilities raises ValueError if config is not set."""
    calc = TestProbabilityCalculator()  # config is None
    with pytest.raises(
        ValueError, match="Config must be set to calculate raw probabilities."
    ):
        calc._calculate_raw_probabilities()


def test_raw_probabilities_logic(probability_calculator, sample_banner_config_for_calc):
    """Test the raw probability calculation logic via initialized state."""
    raw_probs = probability_calculator._calculate_raw_probabilities()
    rolls = np.arange(1, sample_banner_config_for_calc.hard_pity + 1)
    
    assert len(raw_probs) == len(rolls)

    # Check rates before soft pity
    before_soft_pity = raw_probs[:sample_banner_config_for_calc.soft_pity_start_after]
    assert np.allclose(before_soft_pity, sample_banner_config_for_calc.base_rate)

    # Check rates during soft pity
    soft_pity_idx = sample_banner_config_for_calc.soft_pity_start_after
    expected_rate = (
        sample_banner_config_for_calc.base_rate
        + sample_banner_config_for_calc.rate_increase
    )
    assert np.isclose(raw_probs[soft_pity_idx], min(1.0, expected_rate))

    # Check rate at hard pity
    assert raw_probs[-1] == 1.0

    # Validate probabilities
    assert np.all(raw_probs >= 0.0) and np.all(raw_probs <= 1.0)
    ones_idx = np.where(raw_probs == 1.0)[0]
    if len(ones_idx) > 0:
        assert np.all(ones_idx >= sample_banner_config_for_calc.soft_pity_start_after - 1)


def test_first_5star_probabilities(probability_calculator):
    """Test first 5-star probability calculations."""
    raw_probs = probability_calculator._calculate_raw_probabilities()
    first_5star_probs = probability_calculator._calculate_first_5star_prob_from_raw(raw_probs)
    
    # Check array properties
    assert isinstance(first_5star_probs, np.ndarray)
    assert first_5star_probs.dtype == np.float64
    assert len(first_5star_probs) == len(raw_probs)
    
    # Validate probability values
    assert np.all(first_5star_probs >= 0.0)
    assert np.all(first_5star_probs <= 1.0)
    assert np.isclose(np.sum(first_5star_probs), 1.0, atol=1e-5)


def test_cumulative_probabilities(probability_calculator):
    """Test cumulative probability calculations."""
    raw_probs = probability_calculator._calculate_raw_probabilities()
    cumulative_probs = probability_calculator._calculate_cumulative_prob_from_raw(raw_probs)
    
    # Check array properties
    assert isinstance(cumulative_probs, np.ndarray)
    assert cumulative_probs.dtype == np.float64
    assert len(cumulative_probs) == len(raw_probs)
    
    # Validate probability values
    assert np.all(cumulative_probs >= 0.0)
    assert np.all(cumulative_probs <= 1.0)
    
    # Check monotonic increase
    assert np.all(np.diff(cumulative_probs) >= -1e-9)  # Allow for small numerical errors
    
    # Check final probability (hard pity)
    assert np.isclose(cumulative_probs[-1], 1.0)
