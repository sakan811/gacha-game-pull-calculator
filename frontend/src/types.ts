export type GameType = 'genshin' | 'star_rail' | 'zenless';

export type BannerType = 'standard' | 'limited' | 'light_cone' | 'weapon' | 'w_engine';

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