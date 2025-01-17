package banner

import (
	"math"
	"testing"
)

type testCase struct {
	name     string
	testFunc func(*testing.T)
}

func almostEqual(a, b float64) bool {
	return math.Abs(a-b) < 0.0001
}
