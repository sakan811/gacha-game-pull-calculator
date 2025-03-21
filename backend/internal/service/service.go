package service

import (
	"hsrbannercalculator/internal/domain/banner"
)

type BannerService interface {
	CalculateStandardBanner(currentPity, plannedPulls int) (map[string]interface{}, error)
	CalculateLimitedBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error)
	CalculateWeaponBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error)
}

type (
	StarRailService struct{}
	GenshinService  struct{}
	ZenlessService  struct{}
)

func (s *StarRailService) CalculateStandardBanner(currentPity, plannedPulls int) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailStandard, currentPity, plannedPulls, false)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"character_probability":    rateUpProb,
		"light_cone_probability":   rateUpProb,
	}, nil
}

func (s *StarRailService) CalculateLimitedBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLimited, currentPity, plannedPulls, guaranteed)
	standardCharProb := 0.0

	if !guaranteed {
		standardCharProb = baseProb - rateUpProb
	}

	return map[string]interface{}{
		"total_5_star_probability":  baseProb,
		"rate_up_probability":       rateUpProb,
		"standard_char_probability": standardCharProb,
	}, nil
}

func (s *StarRailService) CalculateWeaponBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLightCone, currentPity, plannedPulls, guaranteed)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"rate_up_probability":      rateUpProb,
	}, nil
}

func (s *GenshinService) CalculateStandardBanner(currentPity, plannedPulls int) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinStandard, currentPity, plannedPulls, false)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"character_probability":    rateUpProb,
		"light_cone_probability":   rateUpProb,
	}, nil
}

func (s *GenshinService) CalculateLimitedBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinLimited, currentPity, plannedPulls, guaranteed)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"rate_up_probability":      rateUpProb,
	}, nil
}

func (s *GenshinService) CalculateWeaponBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinWeapon, currentPity, plannedPulls, guaranteed)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"rate_up_probability":      rateUpProb,
	}, nil
}

func (s *ZenlessService) CalculateStandardBanner(currentPity, plannedPulls int) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessStandard, currentPity, plannedPulls, false)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"character_probability":    rateUpProb,
		"light_cone_probability":   rateUpProb,
	}, nil
}

func (s *ZenlessService) CalculateLimitedBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessLimited, currentPity, plannedPulls, guaranteed)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"rate_up_probability":      rateUpProb,
	}, nil
}

func (s *ZenlessService) CalculateWeaponBanner(currentPity, plannedPulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessWEngine, currentPity, plannedPulls, guaranteed)

	return map[string]interface{}{
		"total_5_star_probability": baseProb,
		"rate_up_probability":      rateUpProb,
	}, nil
}

func NewStarRailService() *StarRailService {
	return &StarRailService{}
}

func NewGenshinService() *GenshinService {
	return &GenshinService{}
}

func NewZenlessService() *ZenlessService {
	return &ZenlessService{}
}
