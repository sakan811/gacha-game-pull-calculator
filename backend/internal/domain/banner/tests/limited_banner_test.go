package banner_test

import (
	"hsrbannercalculator/internal/domain/banner"
	"testing"
)

func TestLimitedBanner(t *testing.T) {
	type testCase struct {
		testFunc func(t *testing.T)
		name     string
	}

	tests := []testCase{
		{
			name: "base rates are correct",
			testFunc: func(t *testing.T) {
				config := banner.GetConfig(banner.Limited)
				if config.BaseRate5StarChar != 0.006 {
					t.Errorf("Expected 5★ rate 0.6%%, got %.1f%%", config.BaseRate5StarChar*100)
				}
				if config.BaseRate5StarLC != 0.0 {
					t.Errorf("Expected no light cones, got %.1f%%", config.BaseRate5StarLC*100)
				}
				if config.BaseRate4Star != 0.051 {
					t.Errorf("Expected 4★ rate 5.1%%, got %.1f%%", config.BaseRate4Star*100)
				}
			},
		},
		{
			name: "50/50 rate up mechanics",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.Limited, 0, 1, false)
				standardCharProb := total5StarProb - rateUpProb
				if !almostEqual(rateUpProb, standardCharProb) {
					t.Errorf("Expected equal rate-up and standard probabilities on 50/50, got %.2f%% vs %.2f%%",
						rateUpProb*100, standardCharProb*100)
				}
			},
		},
		{
			name: "guaranteed rate up after losing 50/50",
			testFunc: func(t *testing.T) {
				total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.Limited, 0, 1, true)
				if !almostEqual(rateUpProb, total5StarProb) {
					t.Errorf("Expected 100%% rate-up chance when guaranteed, got %.2f%% vs %.2f%%",
						rateUpProb*100, total5StarProb*100)
				}
			},
		},
		{
			name: "guaranteed 5★ at 90 pulls",
			testFunc: func(t *testing.T) {
				total5StarProb, _ := banner.CalculateWarpProbability(banner.Limited, 89, 1, false)
				if !almostEqual(total5StarProb, 1.0) {
					t.Errorf("Expected 100%% chance at 90 pulls, got %.2f%%", total5StarProb*100)
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, tt.testFunc)
	}
}
