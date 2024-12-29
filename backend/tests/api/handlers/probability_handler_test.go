package handlers

import (
	"encoding/json"
	"hsrbannercalculator/api/calculator"
	"hsrbannercalculator/api/handlers"
	"net/http"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestHandleStandardBannerCalculation(t *testing.T) {
	router := setupTestRouter()
	router.POST("/standard", handlers.HandleStandardBannerCalculation)

	t.Run("valid_request", func(t *testing.T) {
		req := handlers.ProbabilityRequest{
			CurrentPity:  10,
			PlannedPulls: 50,
			Guaranteed:   false,
		}

		w := performRequest(router, "POST", "/standard", req)

		assert.Equal(t, http.StatusOK, w.Code)

		var response calculator.ProbabilityResponse
		err := json.Unmarshal(w.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Greater(t, response.Total5StarProbability, 0.0)
		assert.Greater(t, response.CharacterProbability, 0.0)
		assert.Greater(t, response.LightConeProbability, 0.0)
	})

	t.Run("invalid_request", func(t *testing.T) {
		invalidReq := map[string]string{
			"current_pity": "invalid",
		}

		w := performRequest(router, "POST", "/standard", invalidReq)
		assert.Equal(t, http.StatusBadRequest, w.Code)
	})
}

func TestHandleLimitedBannerCalculation(t *testing.T) {
	router := setupTestRouter()
	router.POST("/limited", handlers.HandleLimitedBannerCalculation)

	t.Run("valid_request_with_guarantee", func(t *testing.T) {
		req := handlers.ProbabilityRequest{
			CurrentPity:  80,
			PlannedPulls: 10,
			Guaranteed:   true,
		}

		w := performRequest(router, "POST", "/limited", req)

		assert.Equal(t, http.StatusOK, w.Code)

		var response calculator.ProbabilityResponse
		err := json.Unmarshal(w.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Greater(t, response.Total5StarProbability, 0.0)
		assert.Greater(t, response.RateUpProbability, 0.0)
	})

	t.Run("valid_request_without_guarantee", func(t *testing.T) {
		req := handlers.ProbabilityRequest{
			CurrentPity:  0,
			PlannedPulls: 90,
			Guaranteed:   false,
		}

		w := performRequest(router, "POST", "/limited", req)
		assert.Equal(t, http.StatusOK, w.Code)
	})
}
