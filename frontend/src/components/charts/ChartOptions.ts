import type { ChartOptions } from "chart.js";
import type { BannerType } from "../../types";

export function createBaseChartOptions(annotations: any): ChartOptions<"line"> {
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: "Probability (%)" },
      },
      x: {
        type: "linear",
        min: 0,
        offset: false,
        grid: { offset: false },
        title: { display: true, text: "Number of Pulls" },
        ticks: { stepSize: 1 },
      },
    },
    plugins: {
      legend: { position: "top" },
      annotation: { annotations },
    },
  };
}

export function getChartAnnotations(
  totalPulls: number,
  bannerType: BannerType,
  softPityStart?: number,
  hardPity?: number,
) {
  return {
    totalPulls: {
      type: "line" as const,
      xMin: totalPulls,
      xMax: totalPulls,
      borderColor: "rgba(255, 0, 0, 0.8)",
      borderWidth: 2,
      borderDash: [6, 6],
      drawTime: "afterDatasetsDraw" as const,
      label: {
        content: `Total Pulls: ${totalPulls}`,
        display: true,
        position: "start" as const,
        backgroundColor: "rgba(255, 255, 255, 0.9)",
        color: "rgb(255, 0, 0)",
        font: { weight: "bold" as const },
        padding: 6,
        yAdjust: -10,
      },
    },
    softPity: {
      type: "line" as const,
      xMin: softPityStart ?? (bannerType === "light_cone" ? 65 : 74),
      xMax: softPityStart ?? (bannerType === "light_cone" ? 65 : 74),
      borderColor: "rgba(255, 165, 0, 0.5)",
      borderWidth: 2,
      borderDash: [5, 5],
      label: {
        content: "Soft Pity",
        position: "start" as const,
        display: true,
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        color: "rgb(255, 165, 0)",
      },
    },
    hardPity: {
      type: "line" as const,
      xMin: hardPity ?? (bannerType === "light_cone" ? 80 : 90),
      xMax: hardPity ?? (bannerType === "light_cone" ? 80 : 90),
      borderColor: "rgba(255, 69, 0, 0.5)",
      borderWidth: 2,
      borderDash: [5, 5],
      label: {
        content: "Hard Pity",
        display: true,
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        color: "rgb(255, 69, 0)",
      },
    },
  };
}
