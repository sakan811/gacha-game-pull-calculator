package services

import (
	"hsrbannercalculator/internal/domain/banner"
)

type VisualizationData struct {
	Rolls                 []int     `json:"rolls"`
	ProbabilityPerRoll    []float64 `json:"probability_per_roll"`
	CumulativeProbability []float64 `json:"cumulative_probability"`
	SoftPityStart         int       `json:"soft_pity_start"`
	HardPity              int       `json:"hard_pity"`
	CurrentPity           int       `json:"current_pity"`
	PlannedPulls          int       `json:"planned_pulls"`
}

func GenerateVisualizationData(bannerType banner.Type, currentPity, plannedPulls int) VisualizationData {
	config := banner.GetConfig(bannerType)

	// Calculate probabilities
	rolls := make([]int, config.HardPity)
	probPerRoll := make([]float64, config.HardPity)
	cumulativeProb := make([]float64, config.HardPity)

	// Calculate probability per roll (chance of getting 5★ on exactly that pull)
	stats := banner.WarpStats{
		Config:       config,
		CurrentPulls: 0,
	}

	prevCumulative := 0.0

	for i := 0; i < config.HardPity; i++ {
		rolls[i] = i + 1
		currentTotal := stats.CalculateWithPity(i + 1)

		// Probability of getting 5★ exactly on this pull
		probPerRoll[i] = currentTotal - prevCumulative

		// Update cumulative probabilities
		cumulativeProb[i] = currentTotal
		prevCumulative = currentTotal
	}

	// Ensure hard pity is 100%
	if len(cumulativeProb) > 0 {
		cumulativeProb[config.HardPity-1] = 1.0
		probPerRoll[config.HardPity-1] = 1.0 - prevCumulative
	}

	return VisualizationData{
		Rolls:                 rolls,
		ProbabilityPerRoll:    probPerRoll,
		CumulativeProbability: cumulativeProb,
		SoftPityStart:         config.SoftPityStart,
		HardPity:              config.HardPity,
		CurrentPity:           currentPity,
		PlannedPulls:          plannedPulls,
	}
}
