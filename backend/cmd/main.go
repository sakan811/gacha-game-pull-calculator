package main

import (
	"fmt"
	"hsrbannercalculator/config"
	"hsrbannercalculator/internal/api/handlers"
	"hsrbannercalculator/internal/constants"
	"hsrbannercalculator/internal/middleware"
	"log"

	"github.com/gin-gonic/gin"
)

func main() {
	cfg := config.LoadConfig()

	r := gin.Default()
	r.Use(middleware.Logger())

	api := r.Group(constants.APIPrefix)

	// Star Rail routes
	starRail := api.Group(constants.StarRailPrefix)
	starRail.POST(constants.StarRailStandard, handlers.HandleStandardBannerCalculation)
	starRail.POST(constants.StarRailLimited, handlers.HandleLimitedBannerCalculation)
	starRail.POST(constants.StarRailLightCone, handlers.HandleLightConeBannerCalculation)

	// Genshin routes
	genshin := api.Group(constants.GenshinPrefix)
	genshin.POST(constants.GenshinStandard, handlers.HandleGenshinStandardBannerCalculation)
	genshin.POST(constants.GenshinLimited, handlers.HandleGenshinLimitedBannerCalculation)
	genshin.POST(constants.GenshinWeapon, handlers.HandleGenshinWeaponBannerCalculation)

	// Zenless Zone Zero routes
	zenless := api.Group(constants.ZenlessPrefix)
	zenless.POST(constants.ZenlessStandard, handlers.HandleZenlessStandardBannerCalculation)
	zenless.POST(constants.ZenlessLimited, handlers.HandleZenlessLimitedBannerCalculation)
	zenless.POST(constants.ZenlessWEngine, handlers.HandleZenlessWEngineBannerCalculation)
	zenless.POST(constants.ZenlessBangboo, handlers.HandleZenlessBangbooBannerCalculation)

	api.POST(constants.Visualization, handlers.HandleVisualizationData)

	// Print the access URL before starting the server
	fmt.Printf("\nWarp Calculator API is running!\nAPI is available at: \033[36mhttp://localhost:%s%s\033[0m\n\n", cfg.Port, constants.APIPrefix)

	// Start the server
	log.Fatal(r.Run(":" + cfg.Port))
}
