package services

import (
	"hsrbannercalculator/internal/api/models"
	"hsrbannercalculator/internal/domain/banner"
)

func CalculateStandardBannerProbability(currentPity, plannedPulls int) models.ProbabilityResponse {
	total5StarProb, characterProb := banner.CalculateWarpProbability(banner.Standard, currentPity, plannedPulls, false)

	return models.ProbabilityResponse{
		Total5StarProbability: total5StarProb * 100,
		CharacterProbability:  characterProb * 100,
		LightConeProbability:  (total5StarProb - characterProb) * 100,
	}
}

func CalculateLimitedBannerProbability(currentPity, plannedPulls int, guaranteed bool) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.Limited, currentPity, plannedPulls, guaranteed)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}

func CalculateLightConeBannerProbability(currentPity, plannedPulls int) models.ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.LightCone, currentPity, plannedPulls, false)

	return models.ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: (total5StarProb - rateUpProb) * 100,
	}
}
