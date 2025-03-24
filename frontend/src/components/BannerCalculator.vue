<template>
  <div class="calculator-layout">
    <div class="top-section">
      <div class="base-container">
        <div class="form-container">
          <div class="form-group">
            <div class="form-input-container">
              <label class="form-label" for="game-type">Game</label>
              <select v-model="gameType" class="form-input" id="game-type">
                <option value="star_rail">Honkai: Star Rail</option>
                <option value="genshin">Genshin Impact</option>
                <option value="zenless">Zenless Zone Zero</option>
              </select>
            </div>

            <div class="form-input-container">
              <label class="form-label" for="banner-type">Banner Type</label>
              <select v-model="bannerType" class="form-input" id="banner-type">
                <option value="standard">Standard Banner</option>
                <option value="limited">Limited Character Banner</option>
                <option v-if="gameType === 'star_rail'" value="light_cone">Light Cone Banner</option>
                <option v-if="gameType === 'genshin'" value="weapon">Weapon Banner</option>
                <option v-if="gameType === 'zenless'" value="w_engine">W-Engine Banner</option>
                <option v-if="gameType === 'zenless'" value="bangboo">Bangboo Banner</option>
              </select>
            </div>

            <div class="form-input-container">
              <label class="form-label" for="pulls">Pulls</label>
              <input
                type="number"
                v-model.number="totalPulls"
                min="1"
                max="200"
                class="form-input"
                id="pulls"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="results-wrapper">
        <ProbabilityResult :result="result" :bannerType="bannerType" :gameType="gameType" />
      </div>
    </div>

    <div class="plots-layout">
      <ProbabilityPlot
        ref="plotRef"
        :bannerType="bannerType"
        :gameType="gameType"
        :totalPulls="totalPulls"
        :result="result"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed, onMounted } from 'vue'
import ProbabilityResult from './ProbabilityResult.vue'
import ProbabilityPlot from './ProbabilityPlot.vue'
import type { ProbabilityPlotMethods } from './types'
import type { GameType, BannerType } from '../types'

interface CalculationResult {
  total_5_star_probability: number
  character_probability?: number
  light_cone_probability?: number
  rate_up_probability?: number
  standard_char_probability?: number
}

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
const plotRef = ref<ProbabilityPlotMethods | null>(null)

// Calculate initial probabilities when component is mounted
onMounted(() => {
  calculateProbability()
})

// Reset banner type when game changes
watch(gameType, () => {
  if (bannerType.value === 'light_cone' && gameType.value !== 'star_rail') {
    bannerType.value = gameType.value === 'genshin' ? 'weapon' : 'w_engine';
  } else if (bannerType.value === 'weapon' && gameType.value !== 'genshin') {
    bannerType.value = gameType.value === 'star_rail' ? 'light_cone' : 'w_engine';
  } else if (bannerType.value === 'w_engine' && gameType.value !== 'zenless') {
    bannerType.value = gameType.value === 'star_rail' ? 'light_cone' : 'weapon';
  }
  calculateProbability()
})

// Watch for changes and validate immediately
watch(totalPulls, (newValue) => {
  if (newValue < 1) totalPulls.value = 1
  if (newValue > 200) totalPulls.value = 200
  calculateProbability()
})

watch(bannerType, () => {
  calculateProbability()
})

const maxPityForBannerType = computed(() => {
  if (gameType.value === 'star_rail') {
    return bannerType.value === 'light_cone' ? 80 : 90
  } else if (gameType.value === 'zenless') {
    return bannerType.value === 'w_engine' || bannerType.value === 'bangboo' ? 80 : 90
  } else {
    // Genshin Impact pity values
    switch (bannerType.value) {
      case 'weapon':
        return 80
      default:
        return 90
    }
  }
})

function validateInputs() {
  // Clamp pulls to valid range
  if (totalPulls.value < 1) totalPulls.value = 1
  if (totalPulls.value > 200) totalPulls.value = 200
}

async function calculateProbability() {
  validateInputs()

  try {
    // Make the API call with the total pulls (no more current pity)
    const response = await fetch(`/api/${gameType.value}/${bannerType.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        current_pity: 0, // Always start at 0 pity
        planned_pulls: totalPulls.value, // Use the total pulls value
        guaranteed: false // Always false for now
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const newResult = await response.json()
    result.value = {
      total_5_star_probability: newResult.total_5_star_probability ?? 0,
      character_probability: newResult.character_probability ?? 0,
      light_cone_probability: newResult.light_cone_probability ?? 0,
      rate_up_probability: newResult.rate_up_probability ?? 0,
      standard_char_probability: newResult.standard_char_probability ?? 0
    }

    // Wait for Vue to update the DOM, then update the charts
    await nextTick()
    await plotRef.value?.updateCharts()
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
</script>

<style>
/* No need to import app.css here as it's imported in main.ts */
</style>