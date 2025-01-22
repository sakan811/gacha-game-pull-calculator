package banner

// Type represents different types of banners in the game
type Type int

const (
	// Star Rail banners
	StarRailStandard Type = iota
	StarRailLimited
	StarRailLightCone

	// Genshin banners
	GenshinStandard
	GenshinLimited
	GenshinWeapon
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
	case StarRailLimited:
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.06,
			RateUpChance:     0.5,
			GuaranteedRateUp: true,
		}
	case StarRailLightCone:
		return Config{
			BaseRate:         0.008, // 0.8%
			FourStarRate:     0.066,
			SoftPityStart:    65,
			HardPity:         80,
			RateIncrease:     0.07,
			RateUpChance:     0.75,
			GuaranteedRateUp: true,
		}
	case GenshinLimited:
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.06,
			RateUpChance:     0.5,
			GuaranteedRateUp: true,
		}
	case GenshinWeapon:
		return Config{
			BaseRate:         0.007, // 0.7%
			FourStarRate:     0.066,
			SoftPityStart:    62,
			HardPity:         80,
			RateIncrease:     0.07,
			RateUpChance:     0.75,
			GuaranteedRateUp: true,
		}
	case GenshinStandard:
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.06,
			RateUpChance:     0.0,
			GuaranteedRateUp: false,
		}
	default: // StarRailStandard
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.06,
			RateUpChance:     0.0,
			GuaranteedRateUp: false,
		}
	}
}

// GetBannerTypeFromGameAndBanner returns the appropriate banner type based on game and banner type strings
func GetBannerTypeFromGameAndBanner(gameType, bannerType string) Type {
	switch {
	case gameType == "star_rail" && bannerType == "standard":
		return StarRailStandard
	case gameType == "star_rail" && bannerType == "limited":
		return StarRailLimited
	case gameType == "star_rail" && bannerType == "light_cone":
		return StarRailLightCone
	case gameType == "genshin" && bannerType == "standard":
		return GenshinStandard
	case gameType == "genshin" && bannerType == "limited":
		return GenshinLimited
	case gameType == "genshin" && bannerType == "weapon":
		return GenshinWeapon
	default:
		return StarRailStandard
	}
}
