<template>
  <div class="plots-wrapper" data-testid="probability-plots">
    <!-- Distribution Chart -->
    <div class="chart-container">
      <h3 class="chart-title">Successful Pull Distribution</h3>
      <div class="chart-canvas-container">
        <Line
          v-if="chartData"
          :key="chartData?.labels?.length ?? 0"
          :data="distributionChartData"
          :options="distributionChartOptions"
        />
      </div>
    </div>

    <!-- Cumulative Chart -->
    <div class="chart-container">
      <h3 class="chart-title">Cumulative Probability</h3>
      <div class="chart-canvas-container">
        <Line
          v-if="chartData"
          :key="chartData?.labels?.length ?? 0"
          :data="cumulativeChartData"
          :options="cumulativeChartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions
} from 'chart.js'
import annotationPlugin from 'chartjs-plugin-annotation'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  annotationPlugin
)

const props = defineProps<{
  bannerType: 'standard' | 'limited' | 'light_cone' | 'weapon' | 'w_engine'
  gameType: 'star_rail' | 'genshin' | 'zenless'
  currentPity: number
  plannedPulls: number
  result: {
    total_5_star_probability: number
  }
}>()

const visualizationData = ref<VisualizationData | null>(null)
const chartData = ref<ChartData | null>(null)

interface VisualizationData {
  rolls: number[];
  probability_per_roll: number[];
  cumulative_probability: number[];
  soft_pity_start: number;
  hard_pity: number;
  current_pity: number;
  planned_pulls: number;
}

async function fetchVisualizationData() {
  try {
    const response = await fetch('/api/visualization', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        game_type: props.gameType,
        banner_type: props.bannerType,
        current_pity: props.currentPity,
        planned_pulls: props.plannedPulls
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json() as VisualizationData
    if (!Array.isArray(data.rolls) || !Array.isArray(data.probability_per_roll) || !Array.isArray(data.cumulative_probability)) {
      throw new Error('Invalid data format received')
    }

    visualizationData.value = data
    chartData.value = {
      labels: data.rolls,
      datasets: [
        {
          label: 'Probability Distribution',
          data: data.probability_per_roll.map(p => p * 100),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        },
        {
          label: 'Cumulative Probability',
          data: data.cumulative_probability.map(p => p * 100),
          borderColor: 'rgb(153, 102, 255)',
          tension: 0.1
        }
      ]
    }
  } catch (error) {
    console.error('Error fetching visualization data:', error)
    // Set empty data on error
    chartData.value = {
      labels: [],
      datasets: [
        {
          label: 'Probability Distribution',
          data: [],
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        },
        {
          label: 'Cumulative Probability',
          data: [],
          borderColor: 'rgb(153, 102, 255)',
          tension: 0.1
        }
      ]
    }
  }
}

// Function to update charts
async function updateCharts() {
  try {
    await fetchVisualizationData()
  } catch (error) {
    console.error('Error fetching visualization data:', error)
  }
}

// Expose update function
defineExpose({ updateCharts })

const distributionChartData = computed<ChartData<'line'>>(() => ({
  labels: chartData.value?.labels ?? [],
  datasets: [{
    label: 'Pull Distribution',
    data: (chartData.value?.datasets[0].data ?? []) as number[],
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1,
    fill: false
  }]
}))

const cumulativeChartData = computed<ChartData<'line'>>(() => ({
  labels: chartData.value?.labels ?? [],
  datasets: [{
    label: 'Cumulative Probability',
    data: (chartData.value?.datasets[1].data ?? []) as number[],
    borderColor: 'rgb(153, 102, 255)',
    tension: 0.1,
    fill: false
  }]
}))

const chartAnnotations = computed(() => ({
  totalPulls: {
    type: 'line' as const,
    xMin: (visualizationData.value?.current_pity ?? 0) + (visualizationData.value?.planned_pulls ?? 0),
    xMax: (visualizationData.value?.current_pity ?? 0) + (visualizationData.value?.planned_pulls ?? 0),
    borderColor: 'rgba(255, 0, 0, 0.8)',
    borderWidth: 2,
    label: {
      content: `Total Pulls: ${(visualizationData.value?.current_pity ?? 0) + (visualizationData.value?.planned_pulls ?? 0)}`,
      display: true,
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      color: 'rgb(255, 0, 0)'
    }
  },
  softPity: {
    type: 'line' as const,
    xMin: visualizationData.value?.soft_pity_start ?? (props.bannerType === 'light_cone' ? 64 : 74),
    xMax: visualizationData.value?.soft_pity_start ?? (props.bannerType === 'light_cone' ? 64 : 74),
    borderColor: 'rgba(255, 165, 0, 0.5)',
    borderWidth: 2,
    borderDash: [5, 5],
    label: {
      content: 'Soft Pity',
      position: 'start' as const,
      display: true,
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      color: 'rgb(255, 165, 0)'
    }
  },
  hardPity: {
    type: 'line' as const,
    xMin: visualizationData.value?.hard_pity ?? 90,
    xMax: visualizationData.value?.hard_pity ?? 90,
    borderColor: 'rgba(255, 69, 0, 0.5)',
    borderWidth: 2,
    borderDash: [5, 5],
    label: {
      content: 'Hard Pity',
      display: true,
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      color: 'rgb(255, 69, 0)'
    }
  }
}))

const baseChartOptions = computed<ChartOptions<'line'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Probability (%)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Number of Pulls'
      }
    }
  },
  plugins: {
    legend: {
      position: 'top'
    },
    annotation: {
      annotations: chartAnnotations.value
    }
  }
}))

const distributionChartOptions = computed<ChartOptions<'line'>>(() => ({
  ...baseChartOptions.value,
  plugins: {
    ...baseChartOptions.value.plugins,
    title: {
      display: true,
      text: 'Probability of getting 5★ at each pull'
    }
  }
}))

const cumulativeChartOptions = computed<ChartOptions<'line'>>(() => ({
  ...baseChartOptions.value,
  plugins: {
    ...baseChartOptions.value.plugins,
    title: {
      display: true,
      text: 'Cumulative probability of getting 5★'
    }
  }
}))
</script>

<style>
/* Styles moved to app.css */
</style> 