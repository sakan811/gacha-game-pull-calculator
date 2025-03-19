package service

import (
	"hsrbannercalculator/internal/domain/banner"
)

type BannerService interface {
	CalculateStandardBanner(pulls int) (map[string]interface{}, error)
	CalculateLimitedBanner(pulls int, guaranteed bool) (map[string]interface{}, error)
	CalculateWeaponBanner(pulls int, guaranteed bool) (map[string]interface{}, error)
}

type (
	StarRailService struct{}
	GenshinService  struct{}
	ZenlessService  struct{}
)

func (s *StarRailService) CalculateStandardBanner(pulls int) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailStandard, 0, pulls, false)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *StarRailService) CalculateLimitedBanner(pulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLimited, 0, pulls, guaranteed)
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

func (s *StarRailService) CalculateWeaponBanner(pulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLightCone, 0, pulls, guaranteed)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *GenshinService) CalculateStandardBanner(pulls int) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinStandard, 0, pulls, false)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *GenshinService) CalculateLimitedBanner(pulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinLimited, 0, pulls, guaranteed)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *GenshinService) CalculateWeaponBanner(pulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinWeapon, 0, pulls, guaranteed)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *ZenlessService) CalculateStandardBanner(pulls int) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessStandard, 0, pulls, false)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *ZenlessService) CalculateLimitedBanner(pulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessLimited, 0, pulls, guaranteed)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
	}, nil
}

func (s *ZenlessService) CalculateWeaponBanner(pulls int, guaranteed bool) (map[string]interface{}, error) {
	baseProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessWEngine, 0, pulls, guaranteed)

	return map[string]interface{}{
		"base_probability":    baseProb,
		"rate_up_probability": rateUpProb,
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
