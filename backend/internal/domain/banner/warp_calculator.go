package banner

import (
	"fmt"
	"math"
)

type WarpStats struct {
	Config
	CurrentPulls int  // Current number of pulls without 5*
	Lost5050     bool // Whether the last 5★ pull lost the 50/50
}

// NewWarpStats creates a new WarpStats instance for the specified banner type.
func NewWarpStats(bannerType Type, currentPulls int, lost5050 bool) WarpStats {
	config := GetConfig(bannerType)
	config.GuaranteedRateUp = lost5050 // Set guaranteed if lost previous 50/50

	return WarpStats{
		Config:       config,
		CurrentPulls: currentPulls,
		Lost5050:     lost5050,
	}
}

// CalculateRateUpProbability calculates chance of getting the rate-up character.
func (w *WarpStats) CalculateRateUpProbability(probability float64) float64 {
	if w.GuaranteedRateUp || w.Lost5050 {
		return probability // 100% rate-up if guaranteed or lost previous 50/50
	}

	return probability * w.RateUpChance // Apply rate-up chance (50% for limited, 75% for light cone)
}

// CalculateWithPity calculates probability including pity system.
func (w *WarpStats) CalculateWithPity(pulls int) float64 {
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

// calculateRateForPull calculates the rate for a specific pull considering pity
func calculateRateForPull(config Config, pullNumber int) float64 {
	rate := config.BaseRate

	// Apply soft pity if applicable
	if pullNumber >= config.SoftPityStart {
		increasedRate := config.BaseRate + float64(pullNumber-config.SoftPityStart+1)*config.RateIncrease
		rate = math.Min(1.0, increasedRate)
	}

	return rate
}

// calculateBaseProbability calculates the base probability for multiple pulls
func calculateBaseProbability(config Config, currentPity, plannedPulls int) float64 {
	// Hard pity check
	if currentPity+plannedPulls >= config.HardPity {
		return 1.0
	}

	// Single pull case
	if plannedPulls == 1 {
		pullNumber := currentPity + 1
		return calculateRateForPull(config, pullNumber)
	}

	// Multiple pulls case
	probability := 0.0
	notGettingBefore := 1.0

	for i := 0; i < plannedPulls; i++ {
		pullNumber := currentPity + i + 1
		currentRate := calculateRateForPull(config, pullNumber)

		probability += notGettingBefore * currentRate
		notGettingBefore *= (1.0 - currentRate)
	}

	return probability
}

// calculateRateUpProbability calculates rate-up probability based on banner type and 50/50 status
func calculateRateUpProbability(bannerType Type, baseProbability float64, lost5050 bool) float64 {
	config := GetConfig(bannerType)

	// For standard banners, character probability is half of total
	if bannerType == StarRailStandard || bannerType == GenshinStandard || bannerType == ZenlessStandard {
		return baseProbability * 0.5
	}

	// For rate-up banners
	if lost5050 {
		return baseProbability // 100% rate-up if guaranteed
	}

	return baseProbability * config.RateUpChance
}

// CalculateWarpProbability calculates the probability of getting a 5* based on current pity.
func CalculateWarpProbability(bannerType Type, currentPity, plannedPulls int, lost5050 bool) (baseProbability, rateUpProbability float64) {
	// For safety, ensure planned pulls is at least 1
	if plannedPulls < 1 {
		plannedPulls = 1
	}

	// Get the banner configuration
	config := GetConfig(bannerType)

	// Calculate base probability
	baseProbability = calculateBaseProbability(config, currentPity, plannedPulls)

	// Calculate rate-up probability
	rateUpProbability = calculateRateUpProbability(bannerType, baseProbability, lost5050)

	// Debug output
	fmt.Printf("Debug - BannerType: %v, CurrentPity: %d, PlannedPulls: %d, BaseProbability: %.4f\n",
		bannerType, currentPity, plannedPulls, baseProbability)

	return
}
