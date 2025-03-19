package banner

import (
	"testing"

	"hsrbannercalculator/internal/domain/banner"
)

func TestStarRailLimitedBanner(t *testing.T) {
	type testCase struct {
		testFunc func(t *testing.T)
		name     string
	}

	tests := []testCase{
		{
			name: "base rates are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLimited)
				if config.BaseRate != 0.006 {
					t.Errorf("Expected base rate 0.6%%, got %.1f%%", config.BaseRate*100)
				}
				if config.FourStarRate != 0.051 {
					t.Errorf("Expected 4★ rate 5.1%%, got %.1f%%", config.FourStarRate*100)
				}
				if config.RateIncrease != 0.07 {
					t.Errorf("Expected rate increase 7%%, got %.1f%%", config.RateIncrease*100)
				}
			},
		},
		{
			name: "pity thresholds are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLimited)
				if config.SoftPityStart != 73 {
					t.Errorf("Expected soft pity at 73, got %d", config.SoftPityStart)
				}
				if config.HardPity != 90 {
					t.Errorf("Expected hard pity at 90, got %d", config.HardPity)
				}
			},
		},
		{
			name: "rate up mechanics are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLimited)
				if config.RateUpChance != 0.5 {
					t.Errorf("Expected 50%% rate-up chance, got %.1f%%", config.RateUpChance*100)
				}
				if !config.GuaranteedRateUp {
					t.Error("Expected guaranteed rate-up to be true")
				}
			},
		},
		{
			name: "50/50 rate up mechanics",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLimited, 0, 1, false)
				if !almostEqual(rateUpProb, total5StarProb*0.5) {
					t.Errorf("Expected rate-up probability to be half of total on 50/50, got %.2f%% vs %.2f%%",
						rateUpProb*100, total5StarProb*50)
				}
			},
		},
		{
			name: "guaranteed rate up after losing 50/50",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLimited, 0, 1, true)
				if !almostEqual(rateUpProb, total5StarProb) {
					t.Errorf("Expected 100%% rate-up chance when guaranteed, got %.2f%% vs %.2f%%",
						rateUpProb*100, total5StarProb*100)
				}
			},
		},
		{
			name: "guaranteed 5★ at 90 pulls",
			testFunc: func(t *testing.T) {
				total5StarProb, _ := banner.CalculateWarpProbability(banner.StarRailLimited, 89, 1, false)
				if !almostEqual(total5StarProb, 1.0) {
					t.Errorf("Expected 100%% chance at 90 pulls, got %.2f%%", total5StarProb*100)
				}
			},
		},
		{
			name: "soft pity increases rates",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.StarRailLimited)
				beforePity, _ := banner.CalculateWarpProbability(banner.StarRailLimited, config.SoftPityStart-1, 1, false)
				afterPity, _ := banner.CalculateWarpProbability(banner.StarRailLimited, config.SoftPityStart, 1, false)
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
