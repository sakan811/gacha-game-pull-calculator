package banner

// BannerType represents different types of banners in the game
type BannerType int

const (
	Standard BannerType = iota
	Limited
	LightCone
)

// BannerConfig holds the configuration for different banner types
type BannerConfig struct {
	BaseRate5StarChar float64 // 0.3% for character
	BaseRate5StarLC   float64 // 0.3% for light cone
	BaseRate4Star     float64 // 5.1%
	SoftPityStart     int
	HardPity          int
	GuaranteedRateUp  bool
	RateUpChance      float64
	CharacterChance   float64
	StandardPoolSize  int
}

// GetBannerConfig returns the configuration for a specific banner type
func GetBannerConfig(bannerType BannerType) BannerConfig {
	switch bannerType {
	case Limited:
		return BannerConfig{
			BaseRate5StarChar: 0.006, // 0.6% (all goes to character)
			BaseRate5StarLC:   0.0,   // No light cones in limited
			BaseRate4Star:     0.051,
			SoftPityStart:     74,
			HardPity:          90,
			RateUpChance:      0.5,
			GuaranteedRateUp:  false,
			CharacterChance:   1.0,
			StandardPoolSize:  7,
		}
	case LightCone:
		return BannerConfig{
			BaseRate5StarChar: 0.0,
			BaseRate5StarLC:   0.008,
			BaseRate4Star:     0.051,
			SoftPityStart:     67,
			HardPity:          80,
			RateUpChance:      0.75,
			GuaranteedRateUp:  false,
			CharacterChance:   0.0,
			StandardPoolSize:  5,
		}
	default: // Standard
		return BannerConfig{
			BaseRate5StarChar: 0.003, // 0.3% for character
			BaseRate5StarLC:   0.003, // 0.3% for light cone
			BaseRate4Star:     0.051,
			SoftPityStart:     74,
			HardPity:          90,
			RateUpChance:      1.0,
			GuaranteedRateUp:  false,
			CharacterChance:   0.5,
			StandardPoolSize:  7,
		}
	}
}
