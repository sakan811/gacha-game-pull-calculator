package banner_test

import (
	"hsrbannercalculator/banner"
	"math"
	"testing"
)

func TestStandardBanner(t *testing.T) {
	t.Run("base rates are correct", func(t *testing.T) {
		config := banner.GetBannerConfig(banner.Standard)
		if config.BaseRate5StarChar != 0.003 {
			t.Errorf("Expected 5★ character rate 0.3%%, got %.1f%%", config.BaseRate5StarChar*100)
		}
		if config.BaseRate5StarLC != 0.003 {
			t.Errorf("Expected 5★ light cone rate 0.3%%, got %.1f%%", config.BaseRate5StarLC*100)
		}
		if config.BaseRate4Star != 0.051 {
			t.Errorf("Expected 4★ rate 5.1%%, got %.1f%%", config.BaseRate4Star*100)
		}
	})

	t.Run("guaranteed 5★ at 90 pulls", func(t *testing.T) {
		total5StarProb, _ := banner.CalculateWarpProbability(banner.Standard, 89, 1, false)
		if !almostEqual(total5StarProb, 1.0) {
			t.Errorf("Expected 100%% chance at 90 pulls, got %.2f%%", total5StarProb*100)
		}
	})

	t.Run("character vs light cone distribution", func(t *testing.T) {
		total5StarProb, characterProb := banner.CalculateWarpProbability(banner.Standard, 0, 1, false)
		lightConeProb := total5StarProb - characterProb
		if !almostEqual(characterProb, lightConeProb) {
			t.Errorf("Expected equal character and light cone probabilities, got %.2f%% vs %.2f%%",
				characterProb*100, lightConeProb*100)
		}
	})
}

func almostEqual(a, b float64) bool {
	const epsilon = 1e-9
	return math.Abs(a-b) < epsilon
}
