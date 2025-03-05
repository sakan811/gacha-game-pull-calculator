package handlers_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"

	"hsrbannercalculator/internal/api/handlers"
)

func TestVisualizationHandler(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.POST("/visualization", handlers.HandleVisualizationData)

	t.Run("should include planned pulls in response", func(t *testing.T) {
		reqBody := map[string]interface{}{
			"game_type":     "star_rail",
			"banner_type":   "standard",
			"current_pity":  10,
			"planned_pulls": 20,
		}
		body, _ := json.Marshal(reqBody)

		w := httptest.NewRecorder()
		req, _ := http.NewRequest("POST", "/visualization", bytes.NewBuffer(body))
		req.Header.Set("Content-Type", "application/json")
		r.ServeHTTP(w, req)

		assert.Equal(t, http.StatusOK, w.Code)

		var response handlers.VisualizationData
		err := json.Unmarshal(w.Body.Bytes(), &response)
		assert.NoError(t, err)

		// Verify planned pulls is included in response
		assert.Equal(t, 20, response.PlannedPulls)
		assert.Equal(t, 10, response.CurrentPity)
	})
}
