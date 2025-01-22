<template>
  <div class="results-container" data-testid="probability-results">
    <h3 class="results-title">Probability Results</h3>
    <dl class="results-text">
      <div class="calculator-wrapper">
        <dt class="form-label">Total 5★ Probability</dt>
        <dd class="text-3xl font-semibold text-indigo-600">
          {{ formatProbability(result.total_5_star_probability) }}%
        </dd>
      </div>

      <template v-if="bannerType === 'standard'">
        <div class="calculator-wrapper">
          <dt class="form-label">Character Probability</dt>
          <dd class="text-3xl font-semibold text-indigo-600">
            {{ formatProbability(result.character_probability) }}%
          </dd>
        </div>
        <div class="calculator-wrapper">
          <dt class="form-label">Light Cone Probability</dt>
          <dd class="text-3xl font-semibold text-indigo-600">
            {{ formatProbability(result.light_cone_probability) }}%
          </dd>
        </div>
      </template>

      <template v-else>
        <div class="calculator-wrapper">
          <dt class="form-label">Rate-Up Probability</dt>
          <dd class="text-3xl font-semibold text-indigo-600">
            {{ formatProbability(result.rate_up_probability) }}%
          </dd>
        </div>
      </template>
    </dl>
  </div>
</template>

<script setup lang="ts">
interface Props {
  result: {
    total_5_star_probability: number
    character_probability?: number
    light_cone_probability?: number
    rate_up_probability?: number
  }
  bannerType: 'standard' | 'limited' | 'light_cone' | 'weapon'
}

defineProps<Props>()

function formatProbability(value?: number): string {
  return value?.toFixed(2) ?? '0.00'
}
</script>

<style scoped>
.results-container {
  @apply mt-8 p-6 bg-blue-50 rounded-md;
}

.results-title {
  @apply text-xl font-semibold text-gray-800 mb-4;
}

.results-text {
  @apply space-y-3 text-base text-gray-600;
}

.calculator-wrapper {
  @apply bg-white rounded-lg shadow-md p-4 mb-4;
}

.form-label {
  @apply block text-base font-medium text-gray-700 mb-2;
}
</style> 