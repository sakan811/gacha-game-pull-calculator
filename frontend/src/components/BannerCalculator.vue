<template>
  <div class="calculator-layout">
    <div class="top-section">
      <div class="calculator-wrapper">
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
              <label class="form-label" for="current-pity">Current Pity</label>
              <input
                type="number"
                v-model.number="currentPity"
                min="0"
                :max="maxPityForBannerType"
                class="form-input"
                id="current-pity"
              />
            </div>

            <div class="form-input-container">
              <label class="form-label" for="planned-pulls">Planned Pulls</label>
              <input
                type="number"
                v-model.number="plannedPulls"
                min="1"
                max="200"
                class="form-input"
                id="planned-pulls"
              />
            </div>
          </div>
        </div>
      </div>

      <div v-if="result" class="results-wrapper">
        <ProbabilityResult :result="result" :bannerType="bannerType" :gameType="gameType" />
      </div>
    </div>

    <div v-if="result" class="plots-layout">
      <ProbabilityPlot
        ref="plotRef"
        :bannerType="bannerType"
        :gameType="gameType"
        :currentPity="currentPity"
        :plannedPulls="plannedPulls"
        :result="result"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue'
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
const currentPity = ref(0)
const plannedPulls = ref(1)
const result = ref<CalculationResult | null>(null)
const plotRef = ref<ProbabilityPlotMethods | null>(null)

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
watch(currentPity, (newValue) => {
  if (newValue < 0) currentPity.value = 0
  if (newValue > maxPityForBannerType.value) currentPity.value = maxPityForBannerType.value
  calculateProbability()
})

watch(plannedPulls, (newValue) => {
  if (newValue < 1) plannedPulls.value = 1
  if (newValue > 200) plannedPulls.value = 200
  calculateProbability()
})

watch(bannerType, () => {
  calculateProbability()
})

const maxPityForBannerType = computed(() => {
  if (gameType.value === 'star_rail') {
    return bannerType.value === 'light_cone' ? 79 : 89
  } else if (gameType.value === 'zenless') {
    return bannerType.value === 'w_engine' || bannerType.value === 'bangboo' ? 79 : 89
  } else {
    // Genshin Impact pity values
    switch (bannerType.value) {
      case 'weapon':
        return 79
      default:
        return 89
    }
  }
})

function validateInputs() {
  // Clamp current pity to valid range
  if (currentPity.value < 0) currentPity.value = 0
  if (currentPity.value > maxPityForBannerType.value) currentPity.value = maxPityForBannerType.value

  // Clamp planned pulls to valid range
  if (plannedPulls.value < 1) plannedPulls.value = 1
  if (plannedPulls.value > 200) plannedPulls.value = 200
}

async function calculateProbability() {
  validateInputs()

  try {
    const response = await fetch(`/api/${gameType.value}/${bannerType.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        current_pity: currentPity.value,
        planned_pulls: plannedPulls.value,
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    result.value = await response.json()
    await nextTick()
    await plotRef.value?.updateCharts()
  } catch (error) {
    console.error('Error:', error)
    result.value = null
  }
}
</script>

<style>
/* No need to import app.css here as it's imported in main.ts */
</style> 