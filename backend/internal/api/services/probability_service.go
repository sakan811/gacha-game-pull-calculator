package services

import (
	"hsrbannercalculator/internal/api/models"
	"hsrbannercalculator/internal/domain/banner"
)

func CalculateStarRailStandardBannerProbability(currentPity, plannedPulls int) models.ProbabilityResponse {
	total5StarProb, characterProb := banner.CalculateWarpProbability(banner.StarRailStandard, currentPity, plannedPulls, false)

	return models.ProbabilityResponse{
		Total5StarProbability: total5StarProb * 100,
		CharacterProbability:  characterProb * 100,
		LightConeProbability:  (total5StarProb - characterProb) * 100,
	}
}

func CalculateStarRailLimitedBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLimited, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}

func CalculateStarRailLightConeBannerProbability(currentPity, plannedPulls int) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.StarRailLightCone, currentPity, plannedPulls, false)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}

func CalculateGenshinStandardBannerProbability(currentPity, plannedPulls int) models.ProbabilityResponse {
	stats := banner.NewWarpStats(banner.GenshinStandard, currentPity, false)
	totalProb := stats.CalculateWithPity(currentPity + plannedPulls)
	characterProb := totalProb * 0.5 // 50% chance for character vs weapon

	return models.ProbabilityResponse{
		Total5StarProbability:   totalProb * 100,
		CharacterProbability:    characterProb * 100,
		LightConeProbability:    characterProb * 100, // Same as character probability for weapons
		StandardCharProbability: characterProb * 100,
	}
}

func CalculateGenshinLimitedBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinLimited, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability: total5StarProb * 100,
		RateUpProbability:     rateUpProb * 100,
	}
}

func CalculateGenshinWeaponBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.GenshinWeapon, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability: total5StarProb * 100,
		RateUpProbability:     rateUpProb * 100,
	}
}

// Zenless Zone Zero banner probability calculations
func CalculateZenlessStandardBannerProbability(currentPity, plannedPulls int) models.ProbabilityResponse {
	stats := banner.NewWarpStats(banner.ZenlessStandard, currentPity, false)
	totalProb := stats.CalculateWithPity(currentPity + plannedPulls)
	characterProb := totalProb * 0.5 // 50% chance for character vs W-Engine

	return models.ProbabilityResponse{
		Total5StarProbability:   totalProb * 100,
		CharacterProbability:    characterProb * 100,
		LightConeProbability:    characterProb * 100, // W-Engine probability (same as character probability)
		StandardCharProbability: characterProb * 100,
	}
}

func CalculateZenlessLimitedBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessLimited, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}

func CalculateZenlessWEngineBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessWEngine, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}

func CalculateZenlessBangbooBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.ZenlessBangboo, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}
