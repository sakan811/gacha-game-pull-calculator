package calculator

import "hsrbannercalculator/banner"

type ProbabilityResponse struct {
	Total5StarProbability   float64 `json:"total_5_star_probability"`
	CharacterProbability    float64 `json:"character_probability"`
	LightConeProbability    float64 `json:"light_cone_probability,omitempty"`
	RateUpProbability       float64 `json:"rate_up_probability,omitempty"`
	StandardCharProbability float64 `json:"standard_char_probability,omitempty"`
}

func CalculateStandardBannerProbability(currentPity, plannedPulls int) ProbabilityResponse {
	total5StarProb, characterProb := banner.CalculateWarpProbability(banner.Standard, currentPity, plannedPulls, false)

	return ProbabilityResponse{
		Total5StarProbability: total5StarProb * 100,
		CharacterProbability:  characterProb * 100,
		LightConeProbability:  (total5StarProb - characterProb) * 100,
	}
}

func CalculateLimitedBannerProbability(currentPity, plannedPulls int, guaranteed bool) ProbabilityResponse {
	total5StarProb, rateUpProb := banner.CalculateWarpProbability(banner.Limited, currentPity, plannedPulls, guaranteed)
	stats := banner.NewWarpStats(banner.Limited, currentPity, guaranteed)
	standardCharProb := stats.CalculateSpecificCharacterProbability(total5StarProb)

	return ProbabilityResponse{
		Total5StarProbability:   total5StarProb * 100,
		RateUpProbability:       rateUpProb * 100,
		StandardCharProbability: standardCharProb * 100,
	}
}
