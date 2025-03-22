package services_test

import (
	"testing"

	"hsrbannercalculator/internal/api/services"

	"github.com/stretchr/testify/assert"
)

func TestCalculateStarRailStandardBannerProbability(t *testing.T) {
	t.Run("low_pity_calculation", func(t *testing.T) {
		result := services.CalculateStarRailStandardBannerProbability(0, 10)
		assert.Less(t, result.Total5StarProbability, 100.0)
		assert.Greater(t, result.Total5StarProbability, 0.0)
		assert.Equal(t, result.CharacterProbability+result.LightConeProbability, result.Total5StarProbability)
	})

	t.Run("high_pity_calculation", func(t *testing.T) {
		result := services.CalculateStarRailStandardBannerProbability(89, 1)
		assert.InDelta(t, 100.0, result.Total5StarProbability, 0.1)
	})
}

func TestCalculateStarRailLimitedBannerProbability(t *testing.T) {
	t.Run("guaranteed_high_pity", func(t *testing.T) {
		result := services.CalculateStarRailLimitedBannerProbability(89, 1, true)
		assert.InDelta(t, 100.0, result.RateUpProbability, 0.1)
	})

	t.Run("non_guaranteed_low_pity", func(t *testing.T) {
		result := services.CalculateStarRailLimitedBannerProbability(0, 10, false)
		assert.Less(t, result.RateUpProbability, result.Total5StarProbability)
		assert.Greater(t, result.StandardCharProbability, 0.0)
	})
}

func TestCalculateStarRailLightConeBannerProbability(t *testing.T) {
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
			result := services.CalculateStarRailLightConeBannerProbability(tt.currentPity, tt.plannedPulls)
			assert.GreaterOrEqual(t, result.Total5StarProbability, tt.wantMin)
			assert.LessOrEqual(t, result.Total5StarProbability, 100.0)
			assert.GreaterOrEqual(t, result.RateUpProbability, 0.0)
			assert.LessOrEqual(t, result.RateUpProbability, result.Total5StarProbability)
		})
	}
}

func TestCalculateGenshinStandardBannerProbability(t *testing.T) {
	t.Run("low_pity_calculation", func(t *testing.T) {
		result := services.CalculateGenshinStandardBannerProbability(0, 10)
		assert.Less(t, result.Total5StarProbability, 100.0)
		assert.Greater(t, result.Total5StarProbability, 0.0)
		assert.Equal(t, result.CharacterProbability+result.LightConeProbability, result.Total5StarProbability)
	})

	t.Run("high_pity_calculation", func(t *testing.T) {
		result := services.CalculateGenshinStandardBannerProbability(89, 1)
		assert.InDelta(t, 100.0, result.Total5StarProbability, 0.1)
	})

	t.Run("character_weapon_equal_probability", func(t *testing.T) {
		result := services.CalculateGenshinStandardBannerProbability(0, 10)
		assert.Equal(t, result.CharacterProbability, result.LightConeProbability)
	})
}

func TestCalculateGenshinLimitedBannerProbability(t *testing.T) {
	t.Run("guaranteed_high_pity", func(t *testing.T) {
		result := services.CalculateGenshinLimitedBannerProbability(89, 1, true)
		assert.InDelta(t, 100.0, result.RateUpProbability, 0.1)
	})

	t.Run("non_guaranteed_low_pity", func(t *testing.T) {
		result := services.CalculateGenshinLimitedBannerProbability(0, 10, false)
		assert.Less(t, result.RateUpProbability, result.Total5StarProbability)
	})

	t.Run("guaranteed_changes_probability", func(t *testing.T) {
		nonGuaranteed := services.CalculateGenshinLimitedBannerProbability(0, 10, false)
		guaranteed := services.CalculateGenshinLimitedBannerProbability(0, 10, true)
		assert.Greater(t, guaranteed.RateUpProbability, nonGuaranteed.RateUpProbability)
	})
}

func TestCalculateGenshinWeaponBannerProbability(t *testing.T) {
	t.Run("guaranteed_high_pity", func(t *testing.T) {
		result := services.CalculateGenshinWeaponBannerProbability(79, 1, true)
		assert.InDelta(t, 100.0, result.RateUpProbability, 0.1)
	})

	t.Run("non_guaranteed_low_pity", func(t *testing.T) {
		result := services.CalculateGenshinWeaponBannerProbability(0, 10, false)
		assert.Less(t, result.RateUpProbability, result.Total5StarProbability)
	})

	t.Run("soft_pity_increases_rates", func(t *testing.T) {
		beforePity := services.CalculateGenshinWeaponBannerProbability(61, 1, false)
		afterPity := services.CalculateGenshinWeaponBannerProbability(62, 1, false)
		assert.Greater(t, afterPity.Total5StarProbability, beforePity.Total5StarProbability)
	})
}

func TestCalculateZenlessStandardBannerProbability(t *testing.T) {
	t.Run("low_pity_calculation", func(t *testing.T) {
		result := services.CalculateZenlessStandardBannerProbability(0, 10)
		assert.Less(t, result.Total5StarProbability, 100.0)
		assert.Greater(t, result.Total5StarProbability, 0.0)
		assert.Equal(t, result.CharacterProbability+result.LightConeProbability, result.Total5StarProbability)
	})

	t.Run("high_pity_calculation", func(t *testing.T) {
		result := services.CalculateZenlessStandardBannerProbability(89, 1)
		assert.InDelta(t, 100.0, result.Total5StarProbability, 0.1)
	})

	t.Run("character_w_engine_equal_probability", func(t *testing.T) {
		result := services.CalculateZenlessStandardBannerProbability(0, 10)
		assert.Equal(t, result.CharacterProbability, result.LightConeProbability)
		assert.Equal(t, result.Total5StarProbability/2, result.CharacterProbability)
	})
}

func TestCalculateZenlessLimitedBannerProbability(t *testing.T) {
	t.Run("guaranteed_high_pity", func(t *testing.T) {
		result := services.CalculateZenlessLimitedBannerProbability(89, 1, true)
		assert.InDelta(t, 100.0, result.RateUpProbability, 0.1)
	})

	t.Run("non_guaranteed_low_pity", func(t *testing.T) {
		result := services.CalculateZenlessLimitedBannerProbability(0, 10, false)
		assert.Less(t, result.RateUpProbability, result.Total5StarProbability)
		assert.Greater(t, result.StandardCharProbability, 0.0)
	})
}

func TestCalculateZenlessWEngineBannerProbability(t *testing.T) {
	tests := []struct {
		name         string
		currentPity  int
		plannedPulls int
		guaranteed   bool
		wantMin      float64 // Minimum expected probability
	}{
		{
			name:         "Before soft pity, not guaranteed",
			currentPity:  50,
			plannedPulls: 10,
			guaranteed:   false,
			wantMin:      0.0,
		},
		{
			name:         "During soft pity, not guaranteed",
			currentPity:  65,
			plannedPulls: 5,
			guaranteed:   false,
			wantMin:      20.0,
		},
		{
			name:         "Near hard pity, guaranteed",
			currentPity:  78,
			plannedPulls: 1,
			guaranteed:   true,
			wantMin:      90.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := services.CalculateZenlessWEngineBannerProbability(tt.currentPity, tt.plannedPulls, tt.guaranteed)
			assert.GreaterOrEqual(t, result.Total5StarProbability, tt.wantMin)
			assert.LessOrEqual(t, result.Total5StarProbability, 100.0)
			assert.GreaterOrEqual(t, result.RateUpProbability, 0.0)
			assert.LessOrEqual(t, result.RateUpProbability, result.Total5StarProbability)
		})
	}
}
