package services_test

import (
	"hsrbannercalculator/internal/api/services"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCalculateStandardBannerProbability(t *testing.T) {
	t.Run("low_pity_calculation", func(t *testing.T) {
		result := services.CalculateStandardBannerProbability(0, 10)
		assert.Less(t, result.Total5StarProbability, 100.0)
		assert.Greater(t, result.Total5StarProbability, 0.0)
		assert.Equal(t, result.CharacterProbability+result.LightConeProbability, result.Total5StarProbability)
	})

	t.Run("high_pity_calculation", func(t *testing.T) {
		result := services.CalculateStandardBannerProbability(89, 1)
		assert.InDelta(t, 100.0, result.Total5StarProbability, 0.1)
	})
}

func TestCalculateLimitedBannerProbability(t *testing.T) {
	t.Run("guaranteed_high_pity", func(t *testing.T) {
		result := services.CalculateLimitedBannerProbability(89, 1, true)
		assert.InDelta(t, 100.0, result.RateUpProbability, 0.1)
	})

	t.Run("non_guaranteed_low_pity", func(t *testing.T) {
		result := services.CalculateLimitedBannerProbability(0, 10, false)
		assert.Less(t, result.RateUpProbability, result.Total5StarProbability)
		assert.Greater(t, result.StandardCharProbability, 0.0)
	})
}

func TestCalculateLightConeBannerProbability(t *testing.T) {
	tests := []struct {
		name         string
		currentPity  int
		plannedPulls int
		wantMin      float64 // Minimum expected probability
	}{
		{
			name:         "Before soft pity",
			currentPity:  50,
			plannedPulls: 10,
			wantMin:      0.0,
		},
		{
			name:         "During soft pity",
			currentPity:  65,
			plannedPulls: 5,
			wantMin:      20.0,
		},
		{
			name:         "Near hard pity",
			currentPity:  78,
			plannedPulls: 1,
			wantMin:      90.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := services.CalculateLightConeBannerProbability(tt.currentPity, tt.plannedPulls)

			assert.GreaterOrEqual(t, result.Total5StarProbability, tt.wantMin)
			assert.LessOrEqual(t, result.Total5StarProbability, 100.0)
			assert.GreaterOrEqual(t, result.RateUpProbability, 0.0)
			assert.LessOrEqual(t, result.RateUpProbability, result.Total5StarProbability)
		})
	}
}
