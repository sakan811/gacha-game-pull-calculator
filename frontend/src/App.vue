<template>
  <div class="main-container">
    <main class="layout-container">
      <h1 class="page-title">Gacha Game Pull Probability Calculator</h1>
      <div class="calculator-centered">
        <BannerCalculator />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import BannerCalculator from './components/BannerCalculator.vue'
</script>

<style scoped>
.main-container {
  @apply min-h-screen bg-gray-50 py-8 px-8 flex justify-center;
}

.layout-container {
  @apply w-full max-w-[1440px] transition-all duration-300 ease-in-out;
}

.calculator-centered {
  @apply flex justify-center w-full;
}

.page-title {
  @apply text-4xl font-bold text-center text-gray-800 mb-8;
}
</style> 