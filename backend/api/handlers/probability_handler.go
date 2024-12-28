package handlers

import (
	"hsrbannercalculator/api/calculator"
	"net/http"

	"github.com/gin-gonic/gin"
)

type ProbabilityRequest struct {
	CurrentPity  int  `json:"current_pity"`
	PlannedPulls int  `json:"planned_pulls"`
	Guaranteed   bool `json:"guaranteed"`
}

func HandleStandardBannerCalculation(c *gin.Context) {
	var req ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := calculator.CalculateStandardBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}

func HandleLimitedBannerCalculation(c *gin.Context) {
	var req ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := calculator.CalculateLimitedBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	c.JSON(http.StatusOK, result)
}
