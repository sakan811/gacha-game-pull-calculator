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
