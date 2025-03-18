package banner

import (
	"testing"

	"hsrbannercalculator/internal/domain/banner"
)

func TestZenlessBangbooBanner(t *testing.T) {
	tests := []testCase{
		{
			name: "base rates are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.ZenlessBangboo)
				if config.BaseRate != 0.01 {
					t.Errorf("Expected base rate 1.0%%, got %.1f%%", config.BaseRate*100)
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
				config := banner.GetConfig(banner.ZenlessBangboo)
				if config.SoftPityStart != 64 {
					t.Errorf("Expected soft pity at 64, got %d", config.SoftPityStart)
				}
				if config.HardPity != 80 {
					t.Errorf("Expected hard pity at 80, got %d", config.HardPity)
				}
			},
		},
		{
			name: "rate up mechanics are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.ZenlessBangboo)
				if config.RateUpChance != 1.0 {
					t.Errorf("Expected 100%% rate-up chance, got %.1f%%", config.RateUpChance*100)
				}
				if !config.GuaranteedRateUp {
					t.Error("Expected guaranteed rate-up to be true")
				}
			},
		},
		{
			name: "guaranteed rate up mechanics",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessBangboo, 0, 1, false)
				if !almostEqual(rateUpProb, total5StarProb) {
					t.Errorf("Expected rate-up probability to be equal to total, got %.2f%% vs %.2f%%",
						rateUpProb*100, total5StarProb*100)
				}
			},
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, tc.testFunc)
	}
}
