<template>
  <div class="base-container" data-testid="probability-results">
    <h3 class="results-title">Probability Results</h3>
    <dl class="results-text">
      <div class="result-item">
        <dt class="form-label">Total 5★ Probability</dt>
        <dd class="result-value">
          {{ formatProbability(result.total_5_star_probability) }}
        </dd>
      </div>

      <template v-if="bannerType === 'standard'">
        <div class="result-item">
          <dt class="form-label">Character Probability</dt>
          <dd class="result-value">
            {{ formatProbability(result.character_probability) }}
          </dd>
        </div>
        <div class="result-item">
          <dt class="form-label">{{ getEquipmentLabel }} Probability</dt>
          <dd class="result-value">
            {{ formatProbability(result.light_cone_probability) }}
          </dd>
        </div>
      </template>

      <template v-else>
        <div class="result-item">
          <dt class="form-label">Rate-Up Probability</dt>
          <dd class="result-value">
            {{ formatProbability(result.rate_up_probability) }}
          </dd>
        </div>
      </template>
    </dl>
  </div>
</template>

<script setup lang="ts">
import type { GameType, BannerType } from '../types'
import { computed } from 'vue'

interface Props {
  result: {
    total_5_star_probability: number
    character_probability?: number
    light_cone_probability?: number
    rate_up_probability?: number
    standard_char_probability?: number
  }
  gameType: GameType
  bannerType: BannerType
}

const props = defineProps<Props>()

const getEquipmentLabel = computed(() => {
  switch (props.gameType) {
    case 'genshin':
      return 'Weapon'
    case 'zenless':
      return 'W-Engine'
    default:
      return 'Light Cone'
  }
})

console.log(props.result)

function formatProbability(value?: number): string {
  if (value === undefined || value === null) return '0.00%';
  // Convert decimal to percentage by multiplying by 100
  return (value * 100).toFixed(2) + '%';
}
</script>