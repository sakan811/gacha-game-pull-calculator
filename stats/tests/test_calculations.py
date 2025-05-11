import pytest
from core.common.errors import ValidationError
from core.calculator import ProbabilityCalculator
from core.config.banner_config import BannerConfig


class TestCalculator:
    @pytest.fixture
    def valid_config(self):
        return BannerConfig(
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

    @pytest.fixture
    def calculator(self, valid_config):
        return ProbabilityCalculator(valid_config)

    def test_config_validation(self, valid_config):
        """Test that calculator works with valid config but not with invalid configs."""
        # With valid config, initialization should succeed
        calculator = ProbabilityCalculator(valid_config)
        assert calculator.config == valid_config

        # Calculator should work with valid config
        try:
            calculator.calculate_probabilities()
        except Exception as e:
            pytest.fail(f"Calculator failed with valid config: {e}")

        # Now test with an invalid config - the validation happens in BannerConfig
        # so we need to create the invalid config differently
        with pytest.raises(ValidationError):
            # This should fail during BannerConfig initialization with validation error
            BannerConfig(
                game_name="Star Rail",
                banner_type="Limited",
                base_rate=2.0,  # Invalid rate > 1.0
                four_star_rate=0.051,
                soft_pity_start_after=73,
                hard_pity=90,
                rate_increase=0.07,
                guaranteed_rate_up=True,
                rate_up_chance=0.5,
            )

    def test_probability_ranges(self, calculator):
        """Test that calculated probabilities are within valid ranges."""
        per_roll, cumulative, first_5star = calculator.calculate_probabilities()

        # Check that all probability values are within valid range [0, 1]
        assert all(0 <= p <= 1 for p in per_roll)
        assert all(0 <= p <= 1 for p in cumulative)
        assert all(0 <= p <= 1 for p in first_5star)

        # Check that cumulative probabilities are monotonically increasing
        for i in range(1, len(cumulative)):
            assert cumulative[i] >= cumulative[i - 1]

        # Check that hard pity works - probability at hard_pity should be approximately 1.0
        # Use pytest.approx() to handle floating point precision issues
        assert per_roll[calculator.config.hard_pity - 1] == pytest.approx(1.0)
        assert cumulative[calculator.config.hard_pity - 1] == pytest.approx(1.0)

    def test_soft_pity_mechanism(self, calculator):
        """Test that soft pity increases probabilities as expected."""
        per_roll, _, _ = calculator.calculate_probabilities()

        # Base rate should be used before soft pity
        for i in range(calculator.config.soft_pity_start_after):
            assert per_roll[i] == calculator.config.base_rate

        # Rates should increase after soft pity starts
        for i in range(
            calculator.config.soft_pity_start_after, calculator.config.hard_pity - 1
        ):
            assert per_roll[i] > calculator.config.base_rate
            # Should also be monotonically increasing during soft pity
            if i > calculator.config.soft_pity_start_after:
                assert per_roll[i] >= per_roll[i - 1]

    def test_calculate_probabilities(self, calculator):
        """Test overall probability calculation."""
        per_roll, cumulative, first_5star = calculator.calculate_probabilities()

        assert len(per_roll) > 0
        assert len(cumulative) > 0
        assert len(first_5star) > 0

        # Probabilities should be valid
        assert all(0 <= p <= 1 for p in per_roll)
        assert all(0 <= p <= 1 for p in cumulative)
        assert all(0 <= p <= 1 for p in first_5star)

        # First value should match base rate with small tolerance for floating point precision
        assert per_roll[0] == pytest.approx(calculator.config.base_rate, abs=1e-6)
