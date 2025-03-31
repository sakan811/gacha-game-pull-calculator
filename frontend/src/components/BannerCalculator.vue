<template>
  <div class="w-full">
    <div class="flex flex-col md:flex-row gap-6 mb-8">
      <div class="w-full md:w-1/2 bg-white rounded-lg shadow p-5">
        <div class="space-y-4">
          <div class="space-y-4">
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700" for="game-type">Game</label>
              <select v-model="gameType" class="w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" id="game-type">
                <option value="star_rail">Honkai: Star Rail</option>
                <option value="genshin">Genshin Impact</option>
                <option value="zenless">Zenless Zone Zero</option>
              </select>
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700" for="banner-type">Banner Type</label>
              <select v-model="bannerType" class="w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" id="banner-type">
                <option value="standard">Standard Banner</option>
                <option value="limited">Limited Character Banner</option>
                <option v-if="gameType === 'star_rail'" value="light_cone">
                  Light Cone Banner
                </option>
                <option v-if="gameType === 'genshin'" value="weapon">
                  Weapon Banner
                </option>
                <option v-if="gameType === 'zenless'" value="w_engine">
                  W-Engine Banner
                </option>
                <option v-if="gameType === 'zenless'" value="bangboo">
                  Bangboo Banner
                </option>
              </select>
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700" for="pulls">Pulls</label>
              <input
                type="number"
                v-model.number="totalPulls"
                :min="1"
                :max="maxPityForBannerType"
                class="w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                id="pulls"
              />
              <small class="text-xs text-gray-500">Max pulls: {{ maxPityForBannerType }}</small>
            </div>
          </div>
        </div>
      </div>
      <div class="w-full md:w-1/2">
        <ProbabilityResult
          :result="result"
          :bannerType="bannerType"
          :gameType="gameType"
        />
      </div>
    </div>
    <div class="w-full px-1">
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
import { ref, watch, nextTick, onMounted } from "vue";
import ProbabilityResult from "./ProbabilityResult.vue";
import ProbabilityPlot from "./ProbabilityPlot.vue";
import type { ProbabilityPlotMethods } from "./types";
import { useBannerCalculator } from "../composables/useBannerCalculator";

const plotRef = ref<ProbabilityPlotMethods | null>(null);
const {
  gameType,
  bannerType,
  totalPulls,
  result,
  maxPityForBannerType,
  calculateProbability,
} = useBannerCalculator();

onMounted(calculateProbability);

watch([gameType, bannerType, totalPulls], async () => {
  await calculateProbability();
  await nextTick();
  await plotRef.value?.updateCharts();
});
</script>
