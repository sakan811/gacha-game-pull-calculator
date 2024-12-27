package banner

import (
	"math"
	"testing"
)

func TestLimitedBanner(t *testing.T) {
	t.Run("base rates are correct", func(t *testing.T) {
		config := GetBannerConfig(Limited)
		if config.BaseRate5StarChar != 0.006 {
			t.Errorf("Expected 5★ rate 0.6%%, got %.1f%%", config.BaseRate5StarChar*100)
		}
		if config.BaseRate5StarLC != 0.0 {
			t.Errorf("Expected no light cones, got %.1f%%", config.BaseRate5StarLC*100)
		}
		if config.BaseRate4Star != 0.051 {
			t.Errorf("Expected 4★ rate 5.1%%, got %.1f%%", config.BaseRate4Star*100)
		}
	})

	t.Run("50/50 rate up mechanics", func(t *testing.T) {
		total5StarProb, rateUpProb := CalculateWarpProbability(Limited, 0, 1, false)
		standardCharProb := total5StarProb - rateUpProb
		if !almostEqual(rateUpProb, standardCharProb) {
			t.Errorf("Expected equal rate-up and standard probabilities on 50/50, got %.2f%% vs %.2f%%",
				rateUpProb*100, standardCharProb*100)
		}
	})

	t.Run("guaranteed rate up after losing 50/50", func(t *testing.T) {
		total5StarProb, rateUpProb := CalculateWarpProbability(Limited, 0, 1, true)
		if !almostEqual(rateUpProb, total5StarProb) {
			t.Errorf("Expected 100%% rate-up chance when guaranteed, got %.2f%% vs %.2f%%",
				rateUpProb*100, total5StarProb*100)
		}
	})

	t.Run("guaranteed 5★ at 90 pulls", func(t *testing.T) {
		total5StarProb, _ := CalculateWarpProbability(Limited, 89, 1, false)
		if !almostEqual(total5StarProb, 1.0) {
			t.Errorf("Expected 100%% chance at 90 pulls, got %.2f%%", total5StarProb*100)
		}
	})

	t.Run("maximum 180 pulls for guaranteed rate-up", func(t *testing.T) {
		// First 5★ at 90 pulls (worst case)
		total5StarProb1, _ := CalculateWarpProbability(Limited, 89, 1, false)
		// Second 5★ at 180 pulls (worst case, after losing 50/50)
		total5StarProb2, rateUpProb2 := CalculateWarpProbability(Limited, 179, 1, true)

		if !almostEqual(total5StarProb1, 1.0) || !almostEqual(total5StarProb2, 1.0) || !almostEqual(rateUpProb2, 1.0) {
			t.Error("Expected guaranteed rate-up character within 180 pulls")
		}
	})
}

// Helper function for floating point comparisons
func almostEqual(a, b float64) bool {
	const epsilon = 1e-9
	return math.Abs(a-b) < epsilon
}
