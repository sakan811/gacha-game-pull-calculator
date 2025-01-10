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
		api.POST("/standard", handlers.HandleStandardBannerCalculation)
		api.POST("/limited", handlers.HandleLimitedBannerCalculation)
		api.POST("/light_cone", handlers.HandleLightConeBannerCalculation)
		api.POST("/visualization", handlers.HandleVisualizationData)
	}

	// Serve embedded static files
	staticFS := embedded.GetFileSystem()
	r.StaticFS("/", staticFS)

	// Print the access URL before starting the server
	fmt.Printf("\nHSR Warp Calculator is running!\nOpen your browser and visit: \033[36mhttp://localhost:8080\033[0m\n\n")

	// Start the server
	log.Fatal(r.Run(":8080"))
}
