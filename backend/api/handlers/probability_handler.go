package handlers

import (
	"encoding/json"
	"hsrbannercalculator/api/calculator"
	"net/http"
)

type ProbabilityRequest struct {
	CurrentPity  int  `json:"current_pity"`
	PlannedPulls int  `json:"planned_pulls"`
	Guaranteed   bool `json:"guaranteed"`
}

func HandleStandardBannerCalculation(w http.ResponseWriter, r *http.Request) {
	var req ProbabilityRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	result := calculator.CalculateStandardBannerProbability(req.CurrentPity, req.PlannedPulls)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(result)
}

func HandleLimitedBannerCalculation(w http.ResponseWriter, r *http.Request) {
	var req ProbabilityRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	result := calculator.CalculateLimitedBannerProbability(req.CurrentPity, req.PlannedPulls, req.Guaranteed)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(result)
}
