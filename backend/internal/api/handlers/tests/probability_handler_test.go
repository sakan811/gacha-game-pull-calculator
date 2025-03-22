package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"hsrbannercalculator/internal/api/handlers"
	"hsrbannercalculator/internal/api/models"

	"github.com/stretchr/testify/assert"
)

func TestHandleStandardBannerCalculation(t *testing.T) {
	router := setupTestRouter()
	router.POST("/standard", handlers.HandleStandardBannerCalculation)

	t.Run("valid_request_base_case", func(t *testing.T) {
		req := models.ProbabilityRequest{
			CurrentPity:  0,
			PlannedPulls: 1,
		}
		w := performRequest(router, "POST", "/standard", req)
		assertValidResponse(t, w, false)
	})

	t.Run("valid_request_soft_pity", func(t *testing.T) {
		req := models.ProbabilityRequest{
			CurrentPity:  75,
			PlannedPulls: 1,
		}
		w := performRequest(router, "POST", "/standard", req)
		assertValidResponse(t, w, false)
	})

	t.Run("valid_request_guaranteed", func(t *testing.T) {
		req := models.ProbabilityRequest{
			CurrentPity:  89,
			PlannedPulls: 1,
		}
		w := performRequest(router, "POST", "/standard", req)
		assertValidResponse(t, w, false)
	})

	t.Run("invalid_request", func(t *testing.T) {
		w := performRequest(router, "POST", "/standard", "invalid")
		assert.Equal(t, http.StatusBadRequest, w.Code)
	})
}

func TestHandleLimitedBannerCalculation(t *testing.T) {
	router := setupTestRouter()
	router.POST("/limited", handlers.HandleLimitedBannerCalculation)

	t.Run("valid_request_base_case", func(t *testing.T) {
		req := models.ProbabilityRequest{
			CurrentPity:  0,
			PlannedPulls: 1,
			Guaranteed:   false,
		}
		w := performRequest(router, "POST", "/limited", req)
		assertValidResponse(t, w, true)
	})

	t.Run("valid_request_guaranteed", func(t *testing.T) {
		req := models.ProbabilityRequest{
			CurrentPity:  89,
			PlannedPulls: 1,
			Guaranteed:   true,
		}
		w := performRequest(router, "POST", "/limited", req)
		assertValidResponse(t, w, true)
	})

	t.Run("invalid_request", func(t *testing.T) {
		w := performRequest(router, "POST", "/limited", "invalid")
		assert.Equal(t, http.StatusBadRequest, w.Code)
	})
}

func TestHandleLightConeBannerCalculation(t *testing.T) {
	router := setupTestRouter()
	router.POST("/light_cone", handlers.HandleLightConeBannerCalculation)

	tests := []struct {
		name           string
		request        models.ProbabilityRequest
		expectedStatus int
	}{
		{
			name: "Valid light cone request",
			request: models.ProbabilityRequest{
				CurrentPity:  65,
				PlannedPulls: 10,
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "Invalid pity for light cone",
			request: models.ProbabilityRequest{
				CurrentPity:  80, // Light cone max pity is 79
				PlannedPulls: 10,
			},
			expectedStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := performRequest(router, "POST", "/light_cone", tt.request)
			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusOK {
				assertValidResponse(t, w, false)
			}
		})
	}
}

func assertValidResponse(t *testing.T, w *httptest.ResponseRecorder, isLimited bool) {
	assert.Equal(t, http.StatusOK, w.Code)

	var response models.ProbabilityResponse
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)

	// Check total probability is valid
	assert.GreaterOrEqual(t, response.Total5StarProbability, 0.0)
	assert.LessOrEqual(t, response.Total5StarProbability, 100.0)

	if isLimited {
		// Limited banner checks
		assert.GreaterOrEqual(t, response.RateUpProbability, 0.0)
		assert.LessOrEqual(t, response.RateUpProbability, response.Total5StarProbability)
		assert.GreaterOrEqual(t, response.StandardCharProbability, 0.0)
	} else {
		// Standard banner checks
		assert.GreaterOrEqual(t, response.CharacterProbability, 0.0)
		assert.GreaterOrEqual(t, response.LightConeProbability, 0.0)
		assert.InDelta(t, response.CharacterProbability, response.LightConeProbability, 0.001)
	}
}
