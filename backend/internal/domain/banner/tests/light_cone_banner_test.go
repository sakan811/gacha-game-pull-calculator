package banner

import (
	"hsrbannercalculator/internal/domain/banner"
	"testing"
)

func TestStarRailLightConeBanner(t *testing.T) {
	tests := []testCase{
		{
			name: "base rates are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLightCone)
				if config.BaseRate != 0.008 {
					t.Errorf("Expected base rate 0.8%%, got %.1f%%", config.BaseRate*100)
				}
				if config.FourStarRate != 0.066 {
					t.Errorf("Expected 4★ rate 6.6%%, got %.1f%%", config.FourStarRate*100)
				}
				if config.RateIncrease != 0.07 {
					t.Errorf("Expected rate increase 7%%, got %.1f%%", config.RateIncrease*100)
				}
			},
		},
		{
			name: "pity thresholds are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLightCone)
				if config.SoftPityStart != 65 {
					t.Errorf("Expected soft pity at 65, got %d", config.SoftPityStart)
				}
				if config.HardPity != 80 {
					t.Errorf("Expected hard pity at 80, got %d", config.HardPity)
				}
			},
		},
		{
			name: "rate up mechanics are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLightCone)
				if config.RateUpChance != 0.75 {
					t.Errorf("Expected 75%% rate-up chance, got %.1f%%", config.RateUpChance*100)
				}
				if !config.GuaranteedRateUp {
					t.Error("Expected guaranteed rate-up to be true")
				}
			},
		},
		{
			name: "75/25 rate up mechanics",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLightCone, 0, 1, false)
				if !almostEqual(rateUpProb, total5StarProb*0.75) {
					t.Errorf("Expected rate-up probability to be 75%% of total, got %.2f%% vs %.2f%%",
						rateUpProb*100, total5StarProb*75)
				}
			},
		},
		{
			name: "guaranteed rate up after losing 75/25",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLightCone, 0, 1, true)
				if !almostEqual(rateUpProb, total5StarProb) {
					t.Errorf("Expected 100%% rate-up chance when guaranteed, got %.2f%% vs %.2f%%",
						rateUpProb*100, total5StarProb*100)
				}
			},
		},
		{
			name: "guaranteed 5★ at 80 pulls",
			testFunc: func(t *testing.T) {
				total5StarProb, _ := banner.CalculateWarpProbability(banner.StarRailLightCone, 79, 1, false)
				if !almostEqual(total5StarProb, 1.0) {
					t.Errorf("Expected 100%% chance at 80 pulls, got %.2f%%", total5StarProb*100)
				}
			},
		},
		{
			name: "soft pity increases rates",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLightCone)
				beforePity, _ := banner.CalculateWarpProbability(banner.StarRailLightCone, config.SoftPityStart-1, 1, false)
				afterPity, _ := banner.CalculateWarpProbability(banner.StarRailLightCone, config.SoftPityStart, 1, false)
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
