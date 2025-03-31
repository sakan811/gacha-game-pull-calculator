<template>
  <div
    class="bg-white rounded-lg shadow p-5 h-full flex flex-col"
    data-testid="probability-results"
  >
    <h3 class="text-xl font-bold text-gray-800 mb-5">Probability Results</h3>
    <dl class="space-y-4 flex-grow flex flex-col justify-evenly">
      <div class="flex flex-col">
        <dt class="text-base font-medium text-gray-700 mb-1">
          Total 5★ Probability
        </dt>
        <dd class="text-3xl font-bold text-blue-600">
          {{ formatProbability(result.total_5_star_probability) }}
        </dd>
      </div>
      <template v-if="bannerType === 'standard'">
        <div class="flex flex-col">
          <dt class="text-base font-medium text-gray-700 mb-1">
            Character Probability
          </dt>
          <dd class="text-2xl font-semibold text-green-600">
            {{ formatProbability(result.character_probability) }}
          </dd>
        </div>
        <div class="flex flex-col">
          <dt class="text-base font-medium text-gray-700 mb-1">
            {{ getEquipmentLabel }} Probability
          </dt>
          <dd class="text-2xl font-semibold text-amber-600">
            {{ formatProbability(result.light_cone_probability) }}
          </dd>
        </div>
      </template>
      <template v-else>
        <div class="flex flex-col">
          <dt class="text-base font-medium text-gray-700 mb-1">
            Rate-Up Probability
          </dt>
          <dd class="text-2xl font-semibold text-purple-600">
            {{ formatProbability(result.rate_up_probability) }}
          </dd>
        </div>
      </template>
    </dl>
  </div>
</template>

<script setup lang="ts">
import type { GameType, BannerType } from "../types";
import { computed } from "vue";

interface Props {
  result: {
    total_5_star_probability: number;
    character_probability?: number;
    light_cone_probability?: number;
    rate_up_probability?: number;
    standard_char_probability?: number;
  };
  gameType: GameType;
  bannerType: BannerType;
}

const props = defineProps<Props>();

const getEquipmentLabel = computed(() => {
  switch (props.gameType) {
    case "genshin":
      return "Weapon";
    case "zenless":
      return "W-Engine";
    default:
      return "Light Cone";
  }
});

function formatProbability(value?: number): string {
  if (value === undefined || value === null) return "0.00%";
  // Convert decimal to percentage by multiplying by 100
  return (value * 100).toFixed(2) + "%";
}
</script>
