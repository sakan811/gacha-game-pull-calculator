package handlers

import (
	"net/http"

	"hsrbannercalculator/internal/api/services"
	"hsrbannercalculator/internal/domain/banner"

	"github.com/gin-gonic/gin"
)

type VisualizationRequest struct {
	GameType     string `json:"game_type"`
	BannerType   string `json:"banner_type"`
	CurrentPity  int    `json:"current_pity"`
	PlannedPulls int    `json:"planned_pulls"`
}

func HandleVisualizationData(c *gin.Context) {
	var req VisualizationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Get banner type from the request
	bannerType := banner.GetBannerTypeFromGameAndBanner(req.GameType, req.BannerType)

	// Validate the current pity
	config := banner.GetConfig(bannerType)
	if req.CurrentPity < 0 || req.CurrentPity > config.HardPity-1 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid current pity"})
		return
	}

	// Get visualization data from service
	data := services.GenerateVisualizationData(bannerType, req.CurrentPity, req.PlannedPulls)
	c.JSON(http.StatusOK, data)
}
