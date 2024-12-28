package main

import (
	"fmt"
	"hsrbannercalculator/api/handlers"
	"hsrbannercalculator/embedded"

	"log"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	// CORS middleware (only needed for development)
	if gin.Mode() != gin.ReleaseMode {
		r.Use(func(c *gin.Context) {
			c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
			c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
			c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type")
			if c.Request.Method == "OPTIONS" {
				c.AbortWithStatus(204)
				return
			}
			c.Next()
		})
	}

	// API routes
	api := r.Group("/api")
	{
		api.POST("/standard", handlers.HandleStandardBannerCalculation)
		api.POST("/limited", handlers.HandleLimitedBannerCalculation)
	}

	// Serve embedded static files
	staticFS := embedded.GetFileSystem()
	r.StaticFS("/", staticFS)

	// Print the access URL before starting the server
	fmt.Printf("\nHSR Warp Calculator is running!\nOpen your browser and visit: \033[36mhttp://localhost:8080\033[0m\n\n")

	// Start the server
	log.Fatal(r.Run(":8080"))
}
