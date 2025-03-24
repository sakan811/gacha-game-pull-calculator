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
import { ref, computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import annotationPlugin from 'chartjs-plugin-annotation'
import type { GameType, BannerType } from '../types'
import { createBaseChartOptions, getChartAnnotations } from './charts/ChartOptions'
import type { VisualizationData, ChartData } from './types'

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

interface Props {
  gameType: GameType
  bannerType: BannerType
  totalPulls: number
  result: {
    total_5_star_probability: number
    character_probability?: number
    light_cone_probability?: number
    rate_up_probability?: number
    standard_char_probability?: number
  }
}

const props = defineProps<Props>()

const visualizationData = ref<VisualizationData | null>(null)
const chartData = ref<ChartData>({
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
})

// Fetch initial visualization data
onMounted(() => {
  fetchVisualizationData()
})

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
        current_pity: 0,
        planned_pulls: props.totalPulls,
        guaranteed: false
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
    // Keep the existing chart data structure but clear the data
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
defineExpose<ProbabilityPlotMethods>({ updateCharts })

const distributionChartData = computed<ChartData<'line'>>(() => ({
  labels: chartData.value?.labels ?? [],
  datasets: [{
    label: 'Pull Distribution',
    data: (chartData.value?.datasets[0].data ?? []).map((y, i) => ({
      x: i + 1,
      y: y as number
    })) as DataPoint[],
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1,
    fill: false,
    parsing: false
  }]
}))

const cumulativeChartData = computed<ChartData<'line'>>(() => ({
  labels: chartData.value?.labels ?? [],
  datasets: [{
    label: 'Cumulative Probability',
    data: (chartData.value?.datasets[1].data ?? []).map((y, i) => ({
      x: i + 1,
      y: y as number
    })) as DataPoint[],
    borderColor: 'rgb(153, 102, 255)',
    tension: 0.1,
    fill: false,
    parsing: false
  }]
}))

const chartAnnotations = computed(() => 
  getChartAnnotations(
    props.totalPulls,
    props.bannerType,
    visualizationData.value?.soft_pity_start,
    visualizationData.value?.hard_pity
  )
)

const baseChartOptions = computed(() => createBaseChartOptions(chartAnnotations.value))

const distributionChartOptions = computed(() => ({
  ...baseChartOptions.value,
  plugins: {
    ...baseChartOptions.value.plugins,
    title: { display: true, text: 'Probability of getting 5★ at each pull' }
  }
}))

const cumulativeChartOptions = computed(() => ({
  ...baseChartOptions.value,
  plugins: {
    ...baseChartOptions.value.plugins,
    title: { display: true, text: 'Cumulative probability of getting 5★' }
  }
}))
</script>

<style>
/* Styles moved to app.css */
</style>