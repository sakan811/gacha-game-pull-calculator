# Tests for core/calculator.py
import pytest
from core.calculator import ProbabilityCalculator
from core.banner import BannerConfig

@pytest.fixture
def sample_banner_config_for_calc():
    """Return a sample BannerConfig for calculator testing."""
    return BannerConfig(
        base_rate=0.006,
        four_star_rate=0.051,  # Not directly used by ProbabilityCalculator methods shown
        soft_pity_start_after=73,
        hard_pity=90,
        rate_increase=0.06,
        guaranteed_rate_up=True, # Not directly used
        rate_up_chance=0.5 # Not directly used
    )

@pytest.fixture
def probability_calculator(sample_banner_config_for_calc):
    """Return a ProbabilityCalculator instance with sample config and rolls."""
    calc = ProbabilityCalculator()
    calc.config = sample_banner_config_for_calc
    calc.rolls = list(range(1, sample_banner_config_for_calc.hard_pity + 1))
    return calc

def test_calculator_initialization(probability_calculator):
    """Test ProbabilityCalculator initialization."""
    assert probability_calculator.probabilities == []
    assert probability_calculator.config is not None
    assert len(probability_calculator.rolls) == probability_calculator.config.hard_pity

def test_calculate_probabilities_before_config_raises_error():
    """Test that _calculate_probabilities raises ValueError if config is not set."""
    calc = ProbabilityCalculator()
    calc.rolls = [1, 2, 3]
    with pytest.raises(ValueError, match="Config must be set to calculate raw probabilities."):
        calc._calculate_raw_probabilities() # Corrected method name

def test_calculate_probabilities_logic(probability_calculator, sample_banner_config_for_calc):
    """Test the _calculate_raw_probabilities method logic."""
    # Manually call to populate self.probabilities for this test,
    # as other methods depend on it.
    probability_calculator.probabilities = probability_calculator._calculate_raw_probabilities() # Corrected method name
    
    assert len(probability_calculator.probabilities) == len(probability_calculator.rolls)

    # Check rates before soft pity
    for i in range(sample_banner_config_for_calc.soft_pity_start_after - 1): # rolls 1 to 72
        assert probability_calculator.probabilities[i] == sample_banner_config_for_calc.base_rate

    # Check rates during soft pity
    idx_soft_pity_first_roll = sample_banner_config_for_calc.soft_pity_start_after # index for roll 74 is 73
    
    expected_rate_roll_74 = (
        sample_banner_config_for_calc.base_rate + 
        (probability_calculator.rolls[idx_soft_pity_first_roll] - sample_banner_config_for_calc.soft_pity_start_after + 1) * 
        sample_banner_config_for_calc.rate_increase
    )
    assert pytest.approx(probability_calculator.probabilities[idx_soft_pity_first_roll]) == expected_rate_roll_74
    
    # Check rate at hard pity (roll 90, index 89)
    assert probability_calculator.probabilities[sample_banner_config_for_calc.hard_pity - 1] == 1.0

    # Check that rates do not exceed 1.0
    for prob in probability_calculator.probabilities:
        assert 0.0 <= prob <= 1.0

def test_calculate_first_5star_prob(probability_calculator):
    """Test the _calculate_first_5star_prob_from_raw method."""
    # Ensure probabilities are calculated first
    probability_calculator.probabilities = probability_calculator._calculate_raw_probabilities() # Corrected method name
    
    first_5star_probs = probability_calculator._calculate_first_5star_prob_from_raw(probability_calculator.probabilities) # Corrected method name
    assert len(first_5star_probs) == len(probability_calculator.rolls)
    
    # Probabilities should be non-negative
    for prob in first_5star_probs:
        assert prob >= 0.0
        
    assert pytest.approx(sum(first_5star_probs), abs=1e-5) == 1.0 

def test_calculate_cumulative_prob(probability_calculator):
    """Test the _calculate_cumulative_prob_from_raw method."""
    # Ensure probabilities are calculated first
    probability_calculator.probabilities = probability_calculator._calculate_raw_probabilities() # Corrected method name
    
    cumulative_probs = probability_calculator._calculate_cumulative_prob_from_raw(probability_calculator.probabilities) # Corrected method name
    assert len(cumulative_probs) == len(probability_calculator.rolls)

    # Cumulative probabilities should be non-decreasing
    for i in range(len(cumulative_probs) - 1):
        assert cumulative_probs[i] <= cumulative_probs[i+1] + 1e-9 # Add tolerance for float comparisons

    # All probabilities should be between 0 and 1
    for prob in cumulative_probs:
        assert 0.0 <= prob <= 1.0
        
    # The last cumulative probability should be 1.0 at hard pity
    assert pytest.approx(cumulative_probs[probability_calculator.config.hard_pity - 1]) == 1.0
