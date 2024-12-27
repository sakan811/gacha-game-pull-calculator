package banner

import (
	"testing"
)

func TestPitySystem(t *testing.T) {
	t.Run("soft pity increases rates", func(t *testing.T) {
		stats := NewWarpStats(Limited, 0, false)
		beforeSoftPity := stats.calculateWithPity(73)
		afterSoftPity := stats.calculateWithPity(75)

		if afterSoftPity <= beforeSoftPity {
			t.Errorf("Expected increased rates after soft pity, got %.2f%% vs %.2f%%",
				afterSoftPity*100, beforeSoftPity*100)
		}
	})

	t.Run("pulls needed calculation", func(t *testing.T) {
		pulls := CalculatePullsNeeded(Limited, 0.99, 0, false)
		if pulls > 90 {
			t.Errorf("Expected maximum 90 pulls needed, got %d", pulls)
		}
	})

	t.Run("cumulative probability increases with pulls", func(t *testing.T) {
		prev := 0.0
		for i := 1; i <= 90; i++ {
			total5StarProb, _ := CalculateWarpProbability(Limited, 0, i, false)
			if total5StarProb < prev {
				t.Errorf("Probability decreased at pull %d: %.2f%% -> %.2f%%",
					i, prev*100, total5StarProb*100)
			}
			prev = total5StarProb
		}
	})
}
