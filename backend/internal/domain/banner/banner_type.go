package banner

// Type represents different types of banners in the game
type Type int

const (
	Standard Type = iota
	Limited
	LightCone
)

// Config holds the configuration for different banner types
type Config struct {
	BaseRate         float64
	FourStarRate     float64
	SoftPityStart    int
	HardPity         int
	RateIncrease     float64
	RateUpChance     float64
	GuaranteedRateUp bool
}

// GetConfig returns the configuration for a specific banner type
func GetConfig(bannerType Type) Config {
	switch bannerType {
	case Limited:
		return Config{
			BaseRate:         0.006,
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.06,
			RateUpChance:     0.5,
			GuaranteedRateUp: true,
		}
	case LightCone:
		return Config{
			BaseRate:         0.008,
			FourStarRate:     0.066,
			SoftPityStart:    65,
			HardPity:         80,
			RateIncrease:     0.07,
			RateUpChance:     0.75,
			GuaranteedRateUp: true,
		}
	default: // Standard
		return Config{
			BaseRate:         0.006,
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.06,
			RateUpChance:     0.0,
			GuaranteedRateUp: false,
		}
	}
}
