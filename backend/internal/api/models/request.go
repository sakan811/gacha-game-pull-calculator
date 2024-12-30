package models

type ProbabilityRequest struct {
	CurrentPity  int  `json:"current_pity"`
	PlannedPulls int  `json:"planned_pulls"`
	Guaranteed   bool `json:"guaranteed"`
}
