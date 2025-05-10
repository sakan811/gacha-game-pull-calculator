# Tests for core/calculator.py
import pytest
from core.calculator import ProbabilityCalculator
from core.banner import BannerConfig

@pytest.fixture
def sample_banner_config_for_calc():
    """Return a sample BannerConfig for calculator testing."""
    return BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=True,
        rate_up_chance=0.5
    )

@pytest.fixture
def probability_calculator(sample_banner_config_for_calc):
    """Return a ProbabilityCalculator instance, initialized with config."""
    calc = ProbabilityCalculator(config=sample_banner_config_for_calc)
    return calc

def test_calculator_initialization_with_config(probability_calculator, sample_banner_config_for_calc):
    """Test ProbabilityCalculator initialization with a config."""
    assert probability_calculator.config == sample_banner_config_for_calc
    assert len(probability_calculator.rolls) == sample_banner_config_for_calc.hard_pity
    assert len(probability_calculator.probabilities) == sample_banner_config_for_calc.hard_pity
    assert len(probability_calculator.p_first_5_star) == sample_banner_config_for_calc.hard_pity
    assert len(probability_calculator.cumulative_prob) == sample_banner_config_for_calc.hard_pity
    assert any(probability_calculator.probabilities)
    assert any(probability_calculator.p_first_5_star)
    assert any(probability_calculator.cumulative_prob)


def test_calculator_initialization_without_config():
    """Test ProbabilityCalculator initialization without a config."""
    calc = ProbabilityCalculator()
    assert calc.config is None
    assert calc.rolls == []
    assert calc.probabilities == []
    assert calc.p_first_5_star == []
    assert calc.cumulative_prob == []

def test_calculate_probabilities_before_config_raises_error():
    """Test that _calculate_raw_probabilities raises ValueError if config is not set."""
    calc = ProbabilityCalculator() # config is None
    with pytest.raises(ValueError, match="Config must be set to calculate raw probabilities."):
        calc._calculate_raw_probabilities()

def test_raw_probabilities_logic(probability_calculator, sample_banner_config_for_calc):
    """Test the raw probability calculation logic via initialized state."""
    assert len(probability_calculator.probabilities) == len(probability_calculator.rolls)

    # Check rates before soft pity
    for i in range(sample_banner_config_for_calc.soft_pity_start_after - 1): # rolls 1 to 72
        assert probability_calculator.probabilities[i] == sample_banner_config_for_calc.base_rate

    # Check rates during soft pity
    idx_soft_pity_first_roll = sample_banner_config_for_calc.soft_pity_start_after # index for roll 74 (e.g. 73)
    
    roll_number_at_idx = probability_calculator.rolls[idx_soft_pity_first_roll] 
    num_increases = roll_number_at_idx - sample_banner_config_for_calc.soft_pity_start_after
    expected_rate_roll_74 = (
        sample_banner_config_for_calc.base_rate +
        num_increases * sample_banner_config_for_calc.rate_increase
    )
    assert pytest.approx(probability_calculator.probabilities[idx_soft_pity_first_roll]) == expected_rate_roll_74
    
    # Check rate at hard pity (roll 90, index 89)
    assert probability_calculator.probabilities[sample_banner_config_for_calc.hard_pity - 1] == 1.0

    # Check that rates do not exceed 1.0 (except at hard pity where it's exactly 1.0)
    for i in range(sample_banner_config_for_calc.hard_pity -1): # Exclude hard pity itself
        assert 0.0 <= probability_calculator.probabilities[i] < 1.0
    assert probability_calculator.probabilities[sample_banner_config_for_calc.hard_pity -1] == 1.0


def test_first_5star_probabilities(probability_calculator):
    """Test the p_first_5_star attribute after initialization."""
    first_5star_probs = probability_calculator.p_first_5_star
    assert len(first_5star_probs) == len(probability_calculator.rolls)
    
    for prob in first_5star_probs:
        assert prob >= 0.0
        
    assert pytest.approx(sum(first_5star_probs), abs=1e-5) == 1.0 

def test_cumulative_probabilities(probability_calculator):
    """Test the cumulative_prob attribute after initialization."""
    cumulative_probs = probability_calculator.cumulative_prob
    assert len(cumulative_probs) == len(probability_calculator.rolls)

    for i in range(len(cumulative_probs) - 1):
        assert cumulative_probs[i] <= cumulative_probs[i+1] + 1e-9 # Add tolerance

    for prob in cumulative_probs:
        assert 0.0 <= prob <= 1.0
        
    assert pytest.approx(cumulative_probs[probability_calculator.config.hard_pity - 1]) == 1.0
