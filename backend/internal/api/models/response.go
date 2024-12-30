package models

type ProbabilityResponse struct {
	Total5StarProbability   float64 `json:"total_5_star_probability"`
	CharacterProbability    float64 `json:"character_probability"`
	LightConeProbability    float64 `json:"light_cone_probability,omitempty"`
	RateUpProbability       float64 `json:"rate_up_probability,omitempty"`
	StandardCharProbability float64 `json:"standard_char_probability,omitempty"`
}
