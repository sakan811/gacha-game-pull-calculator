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

// GetBannerTypeFromGameAndBanner returns a banner type based on game and banner name.
func GetBannerTypeFromGameAndBanner(gameType, bannerType string) Type {
	if gameTypes, ok := bannerTypeMap[gameType]; ok {
		if banner, ok := gameTypes[bannerType]; ok {
			return banner
		}
	}

	return Unknown
}
