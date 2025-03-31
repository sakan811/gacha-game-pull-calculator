<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center py-8 px-4">
    <main class="w-full max-w-6xl bg-white rounded-lg shadow-xl p-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Gacha Game Pull Probability Calculator</h1>
      <div class="flex justify-center">
        <BannerCalculator />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import BannerCalculator from "./components/BannerCalculator.vue";
import "./app.css";
</script>
