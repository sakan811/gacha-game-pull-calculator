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
import { onMounted, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import annotationPlugin from 'chartjs-plugin-annotation'
import { createBaseChartOptions, getChartAnnotations } from './charts/ChartOptions'
import { useChartData } from './charts/useChartData'
import type { ChartProps } from './charts/types'

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement,
  Title, Tooltip, Legend, annotationPlugin
)

const props = defineProps<ChartProps>()

const {
  visualizationData,
  chartData,
  distributionChartData,
  cumulativeChartData,
  fetchVisualizationData
} = useChartData(props)

onMounted(() => fetchVisualizationData())

defineExpose<{ updateCharts: () => Promise<void> }>({ 
  updateCharts: fetchVisualizationData 
})

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