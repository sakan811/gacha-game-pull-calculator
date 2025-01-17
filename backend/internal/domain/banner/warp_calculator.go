package banner

import (
	"math"
)

type WarpStats struct {
	Config
	CurrentPulls int  // Current number of pulls without 5*
	Lost5050     bool // Whether the last 5★ pull lost the 50/50
}

// NewWarpStats creates a new WarpStats instance for the specified banner type
func NewWarpStats(bannerType Type, currentPulls int, lost5050 bool) WarpStats {
	config := GetConfig(bannerType)
	config.GuaranteedRateUp = lost5050 // Set guaranteed if lost previous 50/50
	return WarpStats{
		Config:       config,
		CurrentPulls: currentPulls,
		Lost5050:     lost5050,
	}
}

// CalculateRateUpProbability calculates chance of getting the rate-up character
func (w *WarpStats) calculateRateUpProbability(probability float64) float64 {
	if w.GuaranteedRateUp {
		return probability // 100% rate-up if guaranteed
	}
	return probability * w.RateUpChance // Apply rate-up chance (50% for limited, 75% for light cone)
}

// calculateWithPity calculates probability including pity system
func (w *WarpStats) calculateWithPity(pulls int) float64 {
	if pulls >= w.HardPity {
		return 1.0
	}

	probability := 0.0
	notGettingBefore := 1.0

	for i := 0; i < pulls; i++ {
		currentPull := i + 1
		currentRate := w.BaseRate

		// Apply soft pity
		if currentPull >= w.SoftPityStart {
			increasedRate := w.BaseRate + float64(currentPull-w.SoftPityStart+1)*w.RateIncrease
			currentRate = math.Min(1.0, increasedRate)
		}

		// Probability of getting 5★ on this specific pull
		probability += notGettingBefore * currentRate
		notGettingBefore *= (1.0 - currentRate)
	}

	return probability
}

// CalculateWarpProbability calculates the probability of getting a 5* based on current pity
func CalculateWarpProbability(bannerType Type, currentPulls, plannedPulls int, lost5050 bool) (float64, float64) {
	stats := NewWarpStats(bannerType, currentPulls, lost5050)
	totalPulls := currentPulls + plannedPulls

	// Calculate base 5★ probability
	baseProbability := stats.calculateWithPity(totalPulls)

	if bannerType == Limited || bannerType == LightCone {
		rateUpProb := stats.calculateRateUpProbability(baseProbability)
		return baseProbability, rateUpProb
	}

	// For Standard banner, character probability is exactly half of total
	return baseProbability, baseProbability * 0.5
}
