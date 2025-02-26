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

	result := services.CalculateStarRailStandardBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}

func HandleLimitedBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := services.CalculateStarRailLimitedBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
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

	result := services.CalculateStarRailLightConeBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}

func HandleGenshinStandardBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if req.CurrentPity < 0 || req.CurrentPity > 89 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 89 for Genshin standard banner"})
		return
	}

	result := services.CalculateGenshinStandardBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}

func HandleGenshinLimitedBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if req.CurrentPity < 0 || req.CurrentPity > 89 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 89 for Genshin limited banner"})
		return
	}

	result := services.CalculateGenshinLimitedBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	c.JSON(http.StatusOK, result)
}

func HandleGenshinWeaponBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if req.CurrentPity < 0 || req.CurrentPity > 76 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 76 for Genshin weapon banner"})
		return
	}

	result := services.CalculateGenshinWeaponBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	c.JSON(http.StatusOK, result)
}

// Zenless Zone Zero handlers
func HandleZenlessStandardBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if req.CurrentPity < 0 || req.CurrentPity > 89 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 89 for Zenless standard banner"})
		return
	}

	result := services.CalculateZenlessStandardBannerProbability(req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, result)
}

func HandleZenlessLimitedBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if req.CurrentPity < 0 || req.CurrentPity > 89 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 89 for Zenless limited banner"})
		return
	}

	result := services.CalculateZenlessLimitedBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	c.JSON(http.StatusOK, result)
}

func HandleZenlessWEngineBannerCalculation(c *gin.Context) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if req.CurrentPity < 0 || req.CurrentPity > 79 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "current pity must be between 0 and 79 for Zenless W-Engine banner"})
		return
	}

	result := services.CalculateZenlessWEngineBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	c.JSON(http.StatusOK, result)
}
