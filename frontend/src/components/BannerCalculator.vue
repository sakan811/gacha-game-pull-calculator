<template>
  <div class="calculator-layout">
    <div class="top-section">
      <div class="calculator-wrapper">
        <form @submit.prevent="calculateProbability" class="form-container">
          <div class="form-group">
            <div class="form-input-container">
              <label class="form-label" for="banner-type">Banner Type</label>
              <select v-model="bannerType" class="form-input" id="banner-type">
                <option value="standard">Standard Banner</option>
                <option value="limited">Limited Character Banner</option>
                <option value="light_cone">Light Cone Banner</option>
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

            <button type="submit" class="calculate-button">Calculate</button>
          </div>
        </form>
      </div>

      <div v-if="result" class="results-wrapper">
        <ProbabilityResult :result="result" :bannerType="bannerType" />
      </div>
    </div>

    <div v-if="result" class="plots-layout">
      <ProbabilityPlot
        ref="plotRef"
        :bannerType="bannerType"
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

interface CalculationResult {
  total_5_star_probability: number
  character_probability?: number
  light_cone_probability?: number
  rate_up_probability?: number
  standard_char_probability?: number
}

const bannerType = ref<'standard' | 'limited' | 'light_cone'>('standard')
const currentPity = ref(0)
const plannedPulls = ref(1)
const result = ref<CalculationResult | null>(null)
const plotRef = ref<InstanceType<typeof ProbabilityPlot> | null>(null)

const maxPityForBannerType = computed(() => {
  switch (bannerType.value) {
    case 'light_cone':
      return 79
    default:
      return 89
  }
})

// Watch for changes and validate immediately
watch(currentPity, (newValue) => {
  if (newValue < 0) currentPity.value = 0
  if (newValue > maxPityForBannerType.value) currentPity.value = maxPityForBannerType.value
})

watch(plannedPulls, (newValue) => {
  if (newValue < 1) plannedPulls.value = 1
  if (newValue > 200) plannedPulls.value = 200
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
    const response = await fetch(`/api/${bannerType.value}`, {
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

<style scoped>
.calculator-layout {
  @apply flex flex-col gap-8 w-full max-w-7xl;
}

.top-section {
  @apply flex flex-col md:flex-row gap-8 justify-center;
}

.calculator-wrapper {
  @apply bg-white rounded-lg shadow-md p-8 transition-all duration-300 h-fit md:w-[400px] flex-shrink-0;
}

.results-wrapper {
  @apply flex-1 flex flex-col gap-8 min-w-[300px] md:max-w-[400px];
}

.plots-layout {
  @apply w-full flex flex-col gap-8;
}

.form-container {
  @apply space-y-8;
}

.form-group {
  @apply space-y-6;
}

.form-input-container {
  @apply space-y-2;
}

.form-label {
  @apply block text-base font-medium text-gray-700;
}

.form-input {
  @apply mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-base;
}

.calculate-button {
  @apply w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md 
         hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 
         transition-colors duration-200;
}
</style> 