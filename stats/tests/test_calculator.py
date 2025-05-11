# Tests for core/calculator.py
import pytest
from core.calculator import ProbabilityCalculator
from core.banner import BannerConfig


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
    """Return a ProbabilityCalculator instance, initialized with config."""
    calc = ProbabilityCalculator(config=sample_banner_config_for_calc)
    return calc


def test_calculator_initialization_with_config(
    probability_calculator, sample_banner_config_for_calc
):
    """Test ProbabilityCalculator initialization with a config."""
    assert probability_calculator.config == sample_banner_config_for_calc
    assert len(probability_calculator.rolls) == sample_banner_config_for_calc.hard_pity
    assert (
        len(probability_calculator.probabilities)
        == sample_banner_config_for_calc.hard_pity
    )
    assert (
        len(probability_calculator.p_first_5_star)
        == sample_banner_config_for_calc.hard_pity
    )
    assert (
        len(probability_calculator.cumulative_prob)
        == sample_banner_config_for_calc.hard_pity
    )
    assert any(probability_calculator.probabilities)
    assert any(probability_calculator.p_first_5_star)
    assert any(probability_calculator.cumulative_prob)


def test_calculator_initialization_without_config():
    """Test ProbabilityCalculator initialization without a config."""
    calc = ProbabilityCalculator()
    assert calc.config is None
    assert len(calc.rolls) == 0
    assert len(calc.probabilities) == 0
    assert len(calc.p_first_5_star) == 0
    assert len(calc.cumulative_prob) == 0


def test_calculate_probabilities_before_config_raises_error():
    """Test that _calculate_raw_probabilities raises ValueError if config is not set."""
    calc = ProbabilityCalculator()  # config is None
    with pytest.raises(
        ValueError, match="Config must be set to calculate raw probabilities."
    ):
        calc._calculate_raw_probabilities()


def test_raw_probabilities_logic(probability_calculator, sample_banner_config_for_calc):
    """Test the raw probability calculation logic via initialized state."""
    assert len(probability_calculator.probabilities) == len(
        probability_calculator.rolls
    )

    # Check rates before soft pity (rolls 1 to 72)
    for i in range(sample_banner_config_for_calc.soft_pity_start_after - 1):
        assert (
            probability_calculator.probabilities[i]
            == sample_banner_config_for_calc.base_rate
        )

    # Check rates during soft pity starting at rate_increase
    expected_rate_roll_73 = (
        sample_banner_config_for_calc.base_rate
        + sample_banner_config_for_calc.rate_increase
    )
    assert (
        pytest.approx(
            probability_calculator.probabilities[
                sample_banner_config_for_calc.soft_pity_start_after - 1
            ]
        )
        == expected_rate_roll_73
    )

    # Check rate at hard pity (roll 90, index 89)
    assert (
        probability_calculator.probabilities[
            sample_banner_config_for_calc.hard_pity - 1
        ]
        == 1.0
    )

    # Check that rates are valid probabilities
    for i, prob in enumerate(probability_calculator.probabilities):
        assert 0.0 <= prob <= 1.0  # All probabilities should be in [0,1]
        if prob == 1.0:
            # If we hit probability 1.0, it must be either:
            # 1. At hard pity (index hard_pity - 1)
            # 2. During soft pity when rate_increase accumulation hits 1.0
            assert i >= sample_banner_config_for_calc.soft_pity_start_after - 1, (
                f"Probability 1.0 found before soft pity at index {i}"
            )


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
        assert cumulative_probs[i] <= cumulative_probs[i + 1] + 1e-9  # Add tolerance

    for prob in cumulative_probs:
        assert 0.0 <= prob <= 1.0

    assert (
        pytest.approx(cumulative_probs[probability_calculator.config.hard_pity - 1])
        == 1.0
    )
