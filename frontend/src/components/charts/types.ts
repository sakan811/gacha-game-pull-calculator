import type { GameType, BannerType } from "../../types";

export interface VisualizationData {
  rolls: number[];
  probability_per_roll: number[];
  cumulative_probability: number[];
  soft_pity_start: number;
  hard_pity: number;
  current_pity: number;
  planned_pulls: number;
}

export interface ChartProps {
  gameType: GameType;
  bannerType: BannerType;
  totalPulls: number;
  result: {
    total_5_star_probability: number;
    character_probability?: number;
    light_cone_probability?: number;
    rate_up_probability?: number;
    standard_char_probability?: number;
  };
}

export interface DataPoint {
  x: number;
  y: number;
}
