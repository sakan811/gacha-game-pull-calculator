import { ref, watch, computed } from 'vue'
import type { GameType, BannerType } from '../types'

interface CalculationResult {
  total_5_star_probability: number
  character_probability?: number
  light_cone_probability?: number
  rate_up_probability?: number
  standard_char_probability?: number
}

export function useBannerCalculator() {
  const gameType = ref<GameType>('star_rail')
  const bannerType = ref<BannerType>('standard')
  const totalPulls = ref(1)
  const result = ref<CalculationResult>({
    total_5_star_probability: 0,
    character_probability: 0,
    light_cone_probability: 0,
    rate_up_probability: 0,
    standard_char_probability: 0
  })

  watch(gameType, () => {
    if (bannerType.value === 'light_cone' && gameType.value !== 'star_rail') {
      bannerType.value = gameType.value === 'genshin' ? 'weapon' : 'w_engine'
    } else if (bannerType.value === 'weapon' && gameType.value !== 'genshin') {
      bannerType.value = gameType.value === 'star_rail' ? 'light_cone' : 'w_engine'
    } else if (bannerType.value === 'w_engine' && gameType.value !== 'zenless') {
      bannerType.value = gameType.value === 'star_rail' ? 'light_cone' : 'weapon'
    }
  })

  const maxPityForBannerType = computed(() => {
    if (gameType.value === 'star_rail') {
      return bannerType.value === 'light_cone' ? 80 : 90
    } else if (gameType.value === 'zenless') {
      return bannerType.value === 'w_engine' || bannerType.value === 'bangboo' ? 80 : 90
    } else {
      return bannerType.value === 'weapon' ? 80 : 90
    }
  })

  // Watch totalPulls to validate against maxPity
  watch([totalPulls, maxPityForBannerType], ([pulls, maxPity]) => {
    if (pulls < 1) totalPulls.value = 1
    if (pulls > maxPity) totalPulls.value = maxPity
  })

  async function calculateProbability() {
    if (totalPulls.value < 1) totalPulls.value = 1
    if (totalPulls.value > maxPityForBannerType.value) {
      totalPulls.value = maxPityForBannerType.value
    }

    try {
      const response = await fetch(`/api/${gameType.value}/${bannerType.value}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_pity: 0,
          planned_pulls: totalPulls.value,
          guaranteed: false
        })
      })

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

      const newResult = await response.json()
      result.value = {
        total_5_star_probability: newResult.total_5_star_probability ?? 0,
        character_probability: newResult.character_probability ?? 0,
        light_cone_probability: newResult.light_cone_probability ?? 0,
        rate_up_probability: newResult.rate_up_probability ?? 0,
        standard_char_probability: newResult.standard_char_probability ?? 0
      }
    } catch (error) {
      console.error('Error:', error)
      result.value = {
        total_5_star_probability: 0,
        character_probability: 0,
        light_cone_probability: 0,
        rate_up_probability: 0,
        standard_char_probability: 0
      }
    }
  }

  return {
    gameType,
    bannerType,
    totalPulls,
    result,
    maxPityForBannerType,
    calculateProbability
  }
}
