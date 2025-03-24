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
                :min="1"
                :max="maxPityForBannerType"
                class="form-input"
                id="pulls"
              />
              <small class="form-help">Max pulls: {{ maxPityForBannerType }}</small>
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
import { ref, watch, nextTick, onMounted } from 'vue'
import ProbabilityResult from './ProbabilityResult.vue'
import ProbabilityPlot from './ProbabilityPlot.vue'
import type { ProbabilityPlotMethods } from './types'
import { useBannerCalculator } from '../composables/useBannerCalculator'

const plotRef = ref<ProbabilityPlotMethods | null>(null)
const {
  gameType,
  bannerType,
  totalPulls,
  result,
  maxPityForBannerType,
  calculateProbability
} = useBannerCalculator()

onMounted(calculateProbability)

watch([gameType, bannerType, totalPulls], async () => {
  await calculateProbability()
  await nextTick()
  await plotRef.value?.updateCharts()
})
</script>

<style scoped>
.form-help {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}
</style>