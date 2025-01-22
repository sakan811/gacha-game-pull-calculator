package banner

import (
	"hsrbannercalculator/internal/domain/banner"
	"testing"
)

func TestStarRailStandardBanner(t *testing.T) {
	tests := []testCase{
		{
			name: "base rates are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailStandard)
				if config.BaseRate != 0.006 {
					t.Errorf("Expected base rate 0.6%%, got %.1f%%", config.BaseRate*100)
				}
				if config.FourStarRate != 0.051 {
					t.Errorf("Expected 4★ rate 5.1%%, got %.1f%%", config.FourStarRate*100)
				}
				if config.RateIncrease != 0.06 {
					t.Errorf("Expected rate increase 6%%, got %.1f%%", config.RateIncrease*100)
				}
			},
		},
		{
			name: "pity thresholds are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailStandard)
				if config.SoftPityStart != 73 {
					t.Errorf("Expected soft pity at 73, got %d", config.SoftPityStart)
				}
				if config.HardPity != 90 {
					t.Errorf("Expected hard pity at 90, got %d", config.HardPity)
				}
			},
		},
		{
			name: "guaranteed 5★ at 90 pulls",
			testFunc: func(t *testing.T) {
				total5StarProb, _ := banner.CalculateWarpProbability(banner.StarRailStandard, 89, 1, false)
				if !almostEqual(total5StarProb, 1.0) {
					t.Errorf("Expected 100%% chance at 90 pulls, got %.2f%%", total5StarProb*100)
				}
			},
		},
		{
			name: "character probability is half of total",
			testFunc: func(t *testing.T) {
				total5StarProb, characterProb := banner.CalculateWarpProbability(banner.StarRailStandard, 0, 1, false)
				if !almostEqual(characterProb, total5StarProb*0.5) {
					t.Errorf("Expected character probability to be half of total, got %.2f%% vs %.2f%%",
						characterProb*100, total5StarProb*50)
				}
			},
		},
		{
			name: "soft pity increases rates",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailStandard)
				beforePity, _ := banner.CalculateWarpProbability(banner.StarRailStandard, config.SoftPityStart-1, 1, false)
				afterPity, _ := banner.CalculateWarpProbability(banner.StarRailStandard, config.SoftPityStart, 1, false)
				if afterPity <= beforePity {
					t.Errorf("Expected increased probability after soft pity, got %.2f%% vs %.2f%%",
						afterPity*100, beforePity*100)
				}
			},
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, tc.testFunc)
	}
}
