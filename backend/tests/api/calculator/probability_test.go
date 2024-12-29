package calculator_test

import (
	"hsrbannercalculator/api/calculator"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCalculateStandardBannerProbability(t *testing.T) {
	t.Run("low_pity_calculation", func(t *testing.T) {
		result := calculator.CalculateStandardBannerProbability(0, 10)
		assert.Less(t, result.Total5StarProbability, 100.0)
		assert.Greater(t, result.Total5StarProbability, 0.0)
		assert.Equal(t, result.CharacterProbability+result.LightConeProbability, result.Total5StarProbability)
	})

	t.Run("high_pity_calculation", func(t *testing.T) {
		result := calculator.CalculateStandardBannerProbability(89, 1)
		assert.InDelta(t, 100.0, result.Total5StarProbability, 0.1)
	})
}

func TestCalculateLimitedBannerProbability(t *testing.T) {
	t.Run("guaranteed_high_pity", func(t *testing.T) {
		result := calculator.CalculateLimitedBannerProbability(89, 1, true)
		assert.InDelta(t, 100.0, result.RateUpProbability, 0.1)
	})

	t.Run("non_guaranteed_low_pity", func(t *testing.T) {
		result := calculator.CalculateLimitedBannerProbability(0, 10, false)
		assert.Less(t, result.RateUpProbability, result.Total5StarProbability)
		assert.Greater(t, result.StandardCharProbability, 0.0)
	})
}
