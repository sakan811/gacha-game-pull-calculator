package handlers

import (
	"hsrbannercalculator/internal/api/models"
	"hsrbannercalculator/internal/api/services"
	"net/http"

	"github.com/gin-gonic/gin"
)

func HandleStandardBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := services.CalculateStandardBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}

func HandleLimitedBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := services.CalculateLimitedBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	c.JSON(http.StatusOK, result)
}

func HandleLightConeBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Add validation for light cone pity
	if req.CurrentPity < 0 || req.CurrentPity > 79 { // Light cone has max pity of 79
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 79 for light cone banner"})
		return
	}

	if req.PlannedPulls < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "planned pulls must be at least 1"})
		return
	}

	result := services.CalculateLightConeBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}
