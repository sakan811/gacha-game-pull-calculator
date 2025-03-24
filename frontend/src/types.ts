export type GameType = "genshin" | "star_rail" | "zenless";

export type BannerType =
  | "standard"
  | "limited"
  | "light_cone"
  | "weapon"
  | "w_engine"
  | "bangboo";

export interface BannerRequest {
  current_pity: number;
  planned_pulls: number;
  guaranteed: boolean;
}

export interface BannerResponse {
  total_5_star_probability: number;
  character_probability?: number;
  light_cone_probability?: number;
  rate_up_probability?: number;
  standard_char_probability?: number;
}

export interface CalculateRequest {
  current_pity: number;
  planned_pulls: number;
}

export interface GameBanner {
  id: string;
  name: string;
  type: "character" | "weapon" | "standard";
  baseRate: number;
  softPity: number;
  hardPity: number;
  rateUpGuarantee: boolean;
}

export interface CalculatorInput {
  currentPity: number;
  plannedPulls: number;
  hasGuarantee: boolean;
  selectedGame: string;
  selectedBanner: string;
}

export interface ProbabilityResult {
  overallProbability: number;
  rateUpProbability: number;
  expectedPulls: number;
}
