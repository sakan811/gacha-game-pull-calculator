package banner

import (
	"math"
	"testing"
)

type testCase struct {
	testFunc func(*testing.T)
	name     string
}

func almostEqual(a, b float64) bool {
	return math.Abs(a-b) < 0.0001
}
