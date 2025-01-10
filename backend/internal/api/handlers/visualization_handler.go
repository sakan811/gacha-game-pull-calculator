package handlers

import (
	"hsrbannercalculator/internal/domain/banner"
	"net/http"

	"github.com/gin-gonic/gin"
)

type VisualizationData struct {
	Rolls                 []int     `json:"rolls"`
	ProbabilityPerRoll    []float64 `json:"probability_per_roll"`
	CumulativeProbability []float64 `json:"cumulative_probability"`
	SoftPityStart         int       `json:"soft_pity_start"`
	HardPity              int       `json:"hard_pity"`
	CurrentPity           int       `json:"current_pity"`
}

func HandleVisualizationData(c *gin.Context) {
	var req struct {
		BannerType  string `json:"banner_type"`
		CurrentPity int    `json:"current_pity"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Get banner configuration
	bannerType := banner.Standard
	if req.BannerType == "limited" {
		bannerType = banner.Limited
	} else if req.BannerType == "light_cone" {
		bannerType = banner.LightCone
	}
	config := banner.GetConfig(bannerType)

	// Calculate probabilities
	rolls := make([]int, config.HardPity)
	probPerRoll := make([]float64, config.HardPity)
	cumulativeProb := make([]float64, config.HardPity)

	// Calculate probability per roll (chance of getting 5★ on exactly that pull)
	prevCumulative := 0.0
	for i := 0; i < config.HardPity; i++ {
		rolls[i] = i + 1
		currentTotal, _ := banner.CalculateWarpProbability(bannerType, i, 1, false)

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

	data := VisualizationData{
		Rolls:                 rolls,
		ProbabilityPerRoll:    probPerRoll,
		CumulativeProbability: cumulativeProb,
		SoftPityStart:         config.SoftPityStart,
		HardPity:              config.HardPity,
		CurrentPity:           req.CurrentPity,
	}

	c.JSON(http.StatusOK, data)
}
