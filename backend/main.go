package main

import (
	"hsrbannercalculator/api"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/api/warp", api.HandleWarpCalculation)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
