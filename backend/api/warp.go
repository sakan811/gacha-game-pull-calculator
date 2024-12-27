package api

import (
	"encoding/json"
	"hsrbannercalculator/banner"
	"net/http"
)

type WarpRequest struct {
	BannerType   string `json:"banner_type"` // "standard" or "limited"
	CurrentPity  int    `json:"current_pity"`
	PlannedPulls int    `json:"planned_pulls"`
	GuaranteedUp bool   `json:"guaranteed_up"`
}

type WarpResponse struct {
	Total5StarRate        float64 `json:"total_5_star_rate"`
	RateUpOrCharacterRate float64 `json:"rate_up_or_character_rate"`
}

// HandleWarpCalculation handles the /api/warp endpoint
func HandleWarpCalculation(w http.ResponseWriter, r *http.Request) {
	// Only allow POST method
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Parse request body
	var req WarpRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Validate banner type
	var bannerType banner.BannerType
	switch req.BannerType {
	case "standard":
		bannerType = banner.Standard
	case "limited":
		bannerType = banner.Limited
	default:
		http.Error(w, "Invalid banner type", http.StatusBadRequest)
		return
	}

	// Calculate probabilities
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(
		bannerType,
		req.CurrentPity,
		req.PlannedPulls,
		req.GuaranteedUp,
	)

	// Prepare response
	response := WarpResponse{
		Total5StarRate:        total5StarProb * 100,
		RateUpOrCharacterRate: rateUpProb * 100,
	}

	// Send response
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}
