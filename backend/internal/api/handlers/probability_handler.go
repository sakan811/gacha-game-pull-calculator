package handlers

import (
	"fmt"
	"hsrbannercalculator/internal/api/models"
	"hsrbannercalculator/internal/domain/banner"
	"hsrbannercalculator/internal/errors"
	"hsrbannercalculator/internal/service"
	"net/http"

	"github.com/gin-gonic/gin"
)

var (
	starRailService = service.NewStarRailService()
	genshinService  = service.NewGenshinService()
	zenlessService  = service.NewZenlessService()
)

func validateRequest(c *gin.Context, bannerType banner.Type) (models.ProbabilityRequest, error) {
	var req models.ProbabilityRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		return req, errors.NewInvalidInputError(fmt.Sprintf("invalid request body: %v", err))
	}

	config := banner.GetConfig(bannerType)
	if req.CurrentPity < 0 || req.CurrentPity > config.HardPity-1 {
		return req, errors.NewInvalidPityError(fmt.Sprintf("current pity must be between 0 and %d", config.HardPity-1))
	}

	if req.PlannedPulls < 1 {
		return req, errors.NewInvalidPullsError("planned pulls must be at least 1")
	}

	return req, nil
}

func handleError(c *gin.Context, err error) {
	if appErr, ok := err.(*errors.Error); ok {
		switch appErr.Code {
		case errors.ErrInvalidInput, errors.ErrInvalidPity, errors.ErrInvalidPulls:
			c.JSON(http.StatusBadRequest, gin.H{"error": appErr.Message})
		case errors.ErrInvalidBannerType:
			c.JSON(http.StatusNotFound, gin.H{"error": appErr.Message})
		case errors.ErrCalculation:
			c.JSON(http.StatusInternalServerError, gin.H{"error": appErr.Message})
		default:
			c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
		}

		return
	}

	c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
}

func HandleStandardBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.StarRailStandard)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := starRailService.CalculateStandardBanner(req.CurrentPity, req.PlannedPulls)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleLimitedBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.StarRailLimited)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := starRailService.CalculateLimitedBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleLightConeBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.StarRailLightCone)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := starRailService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.StarRailLightCone)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleGenshinStandardBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.GenshinStandard)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := genshinService.CalculateStandardBanner(req.CurrentPity, req.PlannedPulls)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleGenshinLimitedBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.GenshinLimited)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := genshinService.CalculateLimitedBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleGenshinWeaponBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.GenshinWeapon)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := genshinService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.GenshinWeapon)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

// Zenless Zone Zero handlers.
func HandleZenlessStandardBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.ZenlessStandard)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := zenlessService.CalculateStandardBanner(req.CurrentPity, req.PlannedPulls)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleZenlessLimitedBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.ZenlessLimited)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := zenlessService.CalculateLimitedBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleZenlessWEngineBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.ZenlessWEngine)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := zenlessService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.ZenlessWEngine)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

func HandleZenlessBangbooBannerCalculation(c *gin.Context) {
	req, err := validateRequest(c, banner.ZenlessBangboo)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := zenlessService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.ZenlessBangboo)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}
