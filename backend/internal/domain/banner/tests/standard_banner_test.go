package banner_test

import (
	"hsrbannercalculator/internal/domain/banner"
	"math"
	"testing"
)

func TestStandardBanner(t *testing.T) {
	type testCase struct {
		testFunc func(t *testing.T)
		name     string
	}

	tests := []testCase{
		{
			name: "base rates are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.Standard)
				if config.BaseRate5StarChar != 0.003 {
					t.Errorf("Expected 5★ character rate 0.3%%, got %.1f%%", config.BaseRate5StarChar*100)
				}
				if config.BaseRate5StarLC != 0.003 {
					t.Errorf("Expected 5★ light cone rate 0.3%%, got %.1f%%", config.BaseRate5StarLC*100)
				}
				if config.BaseRate4Star != 0.051 {
					t.Errorf("Expected 4★ rate 5.1%%, got %.1f%%", config.BaseRate4Star*100)
				}
			},
		},
		{
			name: "guaranteed 5★ at 90 pulls",
			testFunc: func(t *testing.T) {
				total5StarProb, _ := banner.CalculateWarpProbability(banner.Standard, 89, 1, false)
				if !almostEqual(total5StarProb, 1.0) {
					t.Errorf("Expected 100%% chance at 90 pulls, got %.2f%%", total5StarProb*100)
				}
			},
		},
		{
			name: "character vs light cone distribution",
			testFunc: func(t *testing.T) {
				total5StarProb, characterProb := banner.CalculateWarpProbability(banner.Standard, 0, 1, false)
				lightConeProb := total5StarProb - characterProb
				if !almostEqual(characterProb, lightConeProb) {
					t.Errorf("Expected equal character and light cone probabilities, got %.2f%% vs %.2f%%",
						characterProb*100, lightConeProb*100)
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, tt.testFunc)
	}
}

func almostEqual(a, b float64) bool {
	const epsilon = 1e-9
	return math.Abs(a-b) < epsilon
}
