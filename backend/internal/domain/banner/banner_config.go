package banner

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

// bannerConfigs stores the configuration for all banner types.
var bannerConfigs = map[Type]Config{
	StarRailLimited: {
		BaseRate:         0.006, // 0.6%
		FourStarRate:     0.051,
		SoftPityStart:    73,
		HardPity:         90,
		RateIncrease:     0.07,
		RateUpChance:     0.5,
		GuaranteedRateUp: true,
	},
	StarRailLightCone: {
		BaseRate:         0.008, // 0.8%
		FourStarRate:     0.066,
		SoftPityStart:    65,
		HardPity:         80,
		RateIncrease:     0.07,
		RateUpChance:     0.75,
		GuaranteedRateUp: true,
	},
	GenshinLimited: {
		BaseRate:         0.006, // 0.6%
		FourStarRate:     0.051,
		SoftPityStart:    73,
		HardPity:         90,
		RateIncrease:     0.07,
		RateUpChance:     0.5,
		GuaranteedRateUp: true,
	},
	GenshinWeapon: {
		BaseRate:         0.007, // 0.7%
		FourStarRate:     0.066,
		SoftPityStart:    62,
		HardPity:         80,
		RateIncrease:     0.07,
		RateUpChance:     0.75,
		GuaranteedRateUp: true,
	},
	GenshinStandard: {
		BaseRate:         0.006, // 0.6%
		FourStarRate:     0.051,
		SoftPityStart:    73,
		HardPity:         90,
		RateIncrease:     0.07,
		RateUpChance:     0.5,
		GuaranteedRateUp: false,
	},
	ZenlessLimited: {
		BaseRate:         0.006, // 0.6%
		FourStarRate:     0.051,
		SoftPityStart:    73,
		HardPity:         90,
		RateIncrease:     0.07,
		RateUpChance:     0.5,
		GuaranteedRateUp: true,
	},
	ZenlessWEngine: {
		BaseRate:         0.01, // 1%
		FourStarRate:     0.08,
		SoftPityStart:    64,
		HardPity:         80,
		RateIncrease:     0.07,
		RateUpChance:     0.75,
		GuaranteedRateUp: true,
	},
	ZenlessStandard: {
		BaseRate:         0.006, // 0.6%
		FourStarRate:     0.051,
		SoftPityStart:    73,
		HardPity:         90,
		RateIncrease:     0.07,
		RateUpChance:     0.5,
		GuaranteedRateUp: false,
	},
	ZenlessBangboo: {
		BaseRate:         0.01, // 1%
		FourStarRate:     0.051,
		SoftPityStart:    64,
		HardPity:         80,
		RateIncrease:     0.07,
		RateUpChance:     1.0,
		GuaranteedRateUp: true,
	},
	StarRailStandard: {
		BaseRate:         0.006, // 0.6%
		FourStarRate:     0.051,
		SoftPityStart:    73,
		HardPity:         90,
		RateIncrease:     0.07,
		RateUpChance:     0.5,
		GuaranteedRateUp: false,
	},
}

// GetConfig returns the configuration for a specific banner type.
func GetConfig(bannerType Type) Config {
	if config, ok := bannerConfigs[bannerType]; ok {
		return config
	}
	// Default to StarRailStandard if unknown type
	return bannerConfigs[StarRailStandard]
}
