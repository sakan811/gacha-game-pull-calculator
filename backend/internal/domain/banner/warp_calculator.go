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

// CalculateWarpProbability calculates the probability of getting a 5* based on current pity.
func CalculateWarpProbability(bannerType Type, currentPity, plannedPulls int, lost5050 bool) (baseProbability, rateUpProbability float64) {
	// Get the banner configuration
	config := GetConfig(bannerType)

	// For safety, make sure the planned pulls is at least 1
	if plannedPulls < 1 {
		plannedPulls = 1
	}

	// Hard pity check - if current pity + planned pulls reaches hard pity, return 100%
	if currentPity+plannedPulls >= config.HardPity {
		baseProbability = 1.0

		// For Standard banner, character probability is exactly half of total
		if bannerType == StarRailStandard || bannerType == GenshinStandard || bannerType == ZenlessStandard {
			rateUpProbability = 0.5
			return
		}

		// For other banners, calculate rate-up probability
		if lost5050 {
			rateUpProbability = 1.0 // Guaranteed if lost previous 50/50
		} else {
			rateUpProbability = config.RateUpChance
		}

		return
	}

	// Handle case where planned pulls is very low (e.g., 1 pull)
	// Need to ensure we calculate base probability for a single pull
	if plannedPulls == 1 {
		// Calculate probability for just one pull
		pullNumber := currentPity + 1
		currentRate := config.BaseRate

		// Apply soft pity if applicable
		if pullNumber >= config.SoftPityStart {
			increasedRate := config.BaseRate + float64(pullNumber-config.SoftPityStart+1)*config.RateIncrease
			currentRate = math.Min(1.0, increasedRate)
		}

		// For a single pull, the probability is just the current rate
		baseProbability = currentRate
	} else {
		// Initialize calculation variables
		probability := 0.0
		notGettingBefore := 1.0

		// Calculate for each planned pull, considering current pity
		for i := 0; i < plannedPulls; i++ {
			// Current pull number including current pity
			pullNumber := currentPity + i + 1
			currentRate := config.BaseRate

			// Apply soft pity if applicable
			if pullNumber >= config.SoftPityStart {
				increasedRate := config.BaseRate + float64(pullNumber-config.SoftPityStart+1)*config.RateIncrease
				currentRate = math.Min(1.0, increasedRate)
			}

			// Calculate probability of getting 5★ on this specific pull
			pullProbability := notGettingBefore * currentRate
			probability += pullProbability

			// Update probability of not getting 5★ before next pull
			notGettingBefore *= (1.0 - currentRate)
		}

		// Set the base probability result
		baseProbability = probability
	}

	// Print debug values to help diagnose issues
	fmt.Printf("Debug - BannerType: %v, CurrentPity: %d, PlannedPulls: %d, BaseProbability: %.4f\n",
		bannerType, currentPity, plannedPulls, baseProbability)

	// For Standard banner, character probability is exactly half of total
	if bannerType == StarRailStandard || bannerType == GenshinStandard || bannerType == ZenlessStandard {
		rateUpProbability = baseProbability * 0.5
		return
	}

	// For other banners with rate-up
	if lost5050 {
		rateUpProbability = baseProbability // 100% rate-up if guaranteed
	} else {
		rateUpProbability = baseProbability * config.RateUpChance
	}

	return
}
