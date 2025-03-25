import { ref, computed, Ref, ComputedRef } from "vue";
import type { ChartData } from "chart.js";
import type { VisualizationData, DataPoint, ChartProps } from "./types";

export function useChartData(props: ChartProps): {
  visualizationData: Ref<VisualizationData | null>;
  chartData: Ref<ChartData>;
  distributionChartData: ComputedRef<ChartData<"line">>;
  cumulativeChartData: ComputedRef<ChartData<"line">>;
  fetchVisualizationData: () => Promise<void>;
} {
  const visualizationData = ref<VisualizationData | null>(null);
  const chartData = ref<ChartData>({
    labels: [],
    datasets: [
      {
        label: "Probability Distribution",
        data: [],
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
      {
        label: "Cumulative Probability",
        data: [],
        borderColor: "rgb(153, 102, 255)",
        tension: 0.1,
      },
    ],
  });

  const distributionChartData = computed<ChartData<"line">>(() => ({
    labels: chartData.value?.labels ?? [],
    datasets: [
      {
        label: "Pull Distribution",
        data: (chartData.value?.datasets[0].data ?? []).map((y, i) => ({
          x: i + 1,
          y: y as number,
        })) as DataPoint[],
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
        fill: false,
        parsing: false,
      },
    ],
  }));

  const cumulativeChartData = computed<ChartData<"line">>(() => ({
    labels: chartData.value?.labels ?? [],
    datasets: [
      {
        label: "Cumulative Probability",
        data: (chartData.value?.datasets[1].data ?? []).map((y, i) => ({
          x: i + 1,
          y: y as number,
        })) as DataPoint[],
        borderColor: "rgb(153, 102, 255)",
        tension: 0.1,
        fill: false,
        parsing: false,
      },
    ],
  }));

  async function fetchVisualizationData() {
    try {
      const response = await fetch("/api/visualization", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          game_type: props.gameType,
          banner_type: props.bannerType,
          current_pity: 0,
          planned_pulls: props.totalPulls,
          guaranteed: false,
        }),
      });

      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      if (
        !Array.isArray(data.rolls) ||
        !Array.isArray(data.probability_per_roll) ||
        !Array.isArray(data.cumulative_probability)
      ) {
        throw new Error("Invalid data format received");
      }

      visualizationData.value = data;
      chartData.value = {
        labels: data.rolls,
        datasets: [
          {
            label: "Probability Distribution",
            data: data.probability_per_roll.map((p: number) => p * 100),
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
          {
            label: "Cumulative Probability",
            data: data.cumulative_probability.map((p: number) => p * 100),
            borderColor: "rgb(153, 102, 255)",
            tension: 0.1,
          },
        ],
      };
    } catch (error) {
      console.error("Error:", error);
      chartData.value = {
        labels: [],
        datasets: [
          {
            label: "Probability Distribution",
            data: [],
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
          {
            label: "Cumulative Probability",
            data: [],
            borderColor: "rgb(153, 102, 255)",
            tension: 0.1,
          },
        ],
      };
    }
  }

  return {
    visualizationData,
    chartData,
    distributionChartData,
    cumulativeChartData,
    fetchVisualizationData,
  };
}
