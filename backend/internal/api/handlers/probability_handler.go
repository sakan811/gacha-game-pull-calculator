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

type bannerHandler struct {
	validateFunc  func(c *gin.Context, bannerType banner.Type) (models.ProbabilityRequest, error)
	calculateFunc func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error)
	bannerType    banner.Type
}

func newBannerHandler(bannerType banner.Type, calculateFunc func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error)) bannerHandler {
	return bannerHandler{
		validateFunc:  validateRequest,
		calculateFunc: calculateFunc,
		bannerType:    bannerType,
	}
}

func (h bannerHandler) Handle(c *gin.Context) {
	req, err := h.validateFunc(c, h.bannerType)
	if err != nil {
		handleError(c, err)
		return
	}

	result, err := h.calculateFunc(req, h.bannerType)
	if err != nil {
		handleError(c, err)
		return
	}

	c.JSON(http.StatusOK, result)
}

// StarRail handlers
func HandleStandardBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return starRailService.CalculateStandardBanner(req.CurrentPity, req.PlannedPulls)
	}
	newBannerHandler(banner.StarRailStandard, calculateFunc).Handle(c)
}

func HandleLimitedBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return starRailService.CalculateLimitedBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	}
	newBannerHandler(banner.StarRailLimited, calculateFunc).Handle(c)
}

func HandleLightConeBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return starRailService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.StarRailLightCone)
	}
	newBannerHandler(banner.StarRailLightCone, calculateFunc).Handle(c)
}

// Genshin handlers
func HandleGenshinStandardBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return genshinService.CalculateStandardBanner(req.CurrentPity, req.PlannedPulls)
	}
	newBannerHandler(banner.GenshinStandard, calculateFunc).Handle(c)
}

func HandleGenshinLimitedBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return genshinService.CalculateLimitedBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	}
	newBannerHandler(banner.GenshinLimited, calculateFunc).Handle(c)
}

func HandleGenshinWeaponBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return genshinService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.GenshinWeapon)
	}
	newBannerHandler(banner.GenshinWeapon, calculateFunc).Handle(c)
}

// Zenless handlers
func HandleZenlessStandardBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return zenlessService.CalculateStandardBanner(req.CurrentPity, req.PlannedPulls)
	}
	newBannerHandler(banner.ZenlessStandard, calculateFunc).Handle(c)
}

func HandleZenlessLimitedBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return zenlessService.CalculateLimitedBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed)
	}
	newBannerHandler(banner.ZenlessLimited, calculateFunc).Handle(c)
}

func HandleZenlessWEngineBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return zenlessService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.ZenlessWEngine)
	}
	newBannerHandler(banner.ZenlessWEngine, calculateFunc).Handle(c)
}

func HandleZenlessBangbooBannerCalculation(c *gin.Context) {
	calculateFunc := func(req models.ProbabilityRequest, bannerType banner.Type) (interface{}, error) {
		return zenlessService.CalculateWeaponBanner(req.CurrentPity, req.PlannedPulls, req.Guaranteed, banner.ZenlessBangboo)
	}
	newBannerHandler(banner.ZenlessBangboo, calculateFunc).Handle(c)
}
