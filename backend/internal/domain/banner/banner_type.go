package banner

// Type represents different types of banners in the game.
type Type int

const (
	Unknown Type = iota
	StarRailStandard
	StarRailLimited
	StarRailLightCone
	GenshinStandard
	GenshinLimited
	GenshinWeapon
	ZenlessStandard
	ZenlessLimited
	ZenlessWEngine
	ZenlessBangboo
)

// Config holds the configuration for different banner types.
type Config struct {
	BaseRate         float64
	FourStarRate     float64
	SoftPityStart    int
	HardPity         int
	RateIncrease     float64
	RateUpChance     float64
	GuaranteedRateUp bool
}

// GetConfig returns the configuration for a specific banner type.
func GetConfig(bannerType Type) Config {
	switch bannerType {
	case StarRailLimited:
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.07,
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
			RateIncrease:     0.07,
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
			RateIncrease:     0.07,
			RateUpChance:     0.0,
			GuaranteedRateUp: false,
		}
	case ZenlessLimited:
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.07,
			RateUpChance:     0.5,
			GuaranteedRateUp: true,
		}
	case ZenlessWEngine:
		return Config{
			BaseRate:         0.01, // 1%
			FourStarRate:     0.08,
			SoftPityStart:    64,
			HardPity:         80,
			RateIncrease:     0.07,
			RateUpChance:     0.75,
			GuaranteedRateUp: true,
		}
	case ZenlessStandard:
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.07,
			RateUpChance:     0.0,
			GuaranteedRateUp: false,
		}
	case ZenlessBangboo:
		return Config{
			BaseRate:         0.01, // 1%
			FourStarRate:     0.051,
			SoftPityStart:    64,
			HardPity:         80,
			RateIncrease:     0.07,
			RateUpChance:     1.0,
			GuaranteedRateUp: true,
		}
	default: // StarRailStandard
		return Config{
			BaseRate:         0.006, // 0.6%
			FourStarRate:     0.051,
			SoftPityStart:    73,
			HardPity:         90,
			RateIncrease:     0.07,
			RateUpChance:     0.0,
			GuaranteedRateUp: false,
		}
	}
}

var bannerTypeMap = map[string]map[string]Type{
	"star_rail": {
		"standard":   StarRailStandard,
		"limited":    StarRailLimited,
		"light_cone": StarRailLightCone,
	},
	"genshin": {
		"standard": GenshinStandard,
		"limited":  GenshinLimited,
		"weapon":   GenshinWeapon,
	},
	"zenless": {
		"standard": ZenlessStandard,
		"limited":  ZenlessLimited,
		"w_engine": ZenlessWEngine,
		"bangboo":  ZenlessBangboo,
	},
}

func GetBannerTypeFromGameAndBanner(gameType, bannerType string) Type {
	if gameTypes, ok := bannerTypeMap[gameType]; ok {
		if banner, ok := gameTypes[bannerType]; ok {
			return banner
		}
	}

	return Unknown
}
