package banner

import (
	"testing"

	"hsrbannercalculator/internal/domain/banner"
)

func TestGetBannerTypeFromGameAndBanner(t *testing.T) {
	tests := []struct {
		name       string
		gameType   string
		bannerType string
		want       banner.Type
	}{
		{
			name:       "star rail standard banner",
			gameType:   "star_rail",
			bannerType: "standard",
			want:       banner.StarRailStandard,
		},
		{
			name:       "star rail limited banner",
			gameType:   "star_rail",
			bannerType: "limited",
			want:       banner.StarRailLimited,
		},
		{
			name:       "star rail light cone banner",
			gameType:   "star_rail",
			bannerType: "light_cone",
			want:       banner.StarRailLightCone,
		},
		{
			name:       "genshin standard banner",
			gameType:   "genshin",
			bannerType: "standard",
			want:       banner.GenshinStandard,
		},
		{
			name:       "genshin limited banner",
			gameType:   "genshin",
			bannerType: "limited",
			want:       banner.GenshinLimited,
		},
		{
			name:       "genshin weapon banner",
			gameType:   "genshin",
			bannerType: "weapon",
			want:       banner.GenshinWeapon,
		},
		{
			name:       "invalid game type",
			gameType:   "invalid",
			bannerType: "standard",
			want:       banner.Unknown,
		},
		{
			name:       "invalid banner type",
			gameType:   "star_rail",
			bannerType: "invalid",
			want:       banner.Unknown,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := banner.GetBannerTypeFromGameAndBanner(tt.gameType, tt.bannerType)
			if got != tt.want {
				t.Errorf("GetBannerTypeFromGameAndBanner(%q, %q) = %v, want %v",
					tt.gameType, tt.bannerType, got, tt.want)
			}
		})
	}
}
