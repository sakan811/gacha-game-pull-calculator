package main

import (
	"fmt"
	"hsrbannercalculator/internal/api/handlers"
	"hsrbannercalculator/internal/web/embedded"
	"log"

	"github.com/gin-gonic/gin"
)

func main() {
	// Set Gin to release mode
	gin.SetMode(gin.ReleaseMode)

	r := gin.Default()

	// API routes
	api := r.Group("/api")
	{
		// Star Rail routes
		starRail := api.Group("/star_rail")
		{
			starRail.POST("/standard", handlers.HandleStandardBannerCalculation)
			starRail.POST("/limited", handlers.HandleLimitedBannerCalculation)
			starRail.POST("/light_cone", handlers.HandleLightConeBannerCalculation)
		}

		// Genshin routes
		genshin := api.Group("/genshin")
		{
			genshin.POST("/standard", handlers.HandleGenshinStandardBannerCalculation)
			genshin.POST("/limited", handlers.HandleGenshinLimitedBannerCalculation)
			genshin.POST("/weapon", handlers.HandleGenshinWeaponBannerCalculation)
		}

		api.POST("/visualization", handlers.HandleVisualizationData)
	}

	// Serve embedded static files
	staticFS := embedded.GetFileSystem()
	r.StaticFS("/", staticFS)

	// Ensure index.html is served for all unmatched routes
	r.NoRoute(func(c *gin.Context) {
		c.FileFromFS("/index.html", staticFS)
	})

	// Print the access URL before starting the server
	fmt.Printf("\nWarp Calculator is running!\nOpen your browser and visit: \033[36mhttp://localhost:8080\033[0m\n\n")

	// Start the server
	log.Fatal(r.Run(":8080"))
}
