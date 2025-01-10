<script lang="ts">
  import Chart from 'chart.js/auto';
  import annotationPlugin from 'chartjs-plugin-annotation';
  Chart.register(annotationPlugin);
  
  export let bannerType: string;
  export let currentPity: number;
  export let plannedPulls: number;
  export let result: any;
  
  let cumulativeChartCanvas: HTMLCanvasElement;
  let distributionChartCanvas: HTMLCanvasElement;
  let cumulativeChart: Chart;
  let distributionChart: Chart;

  async function fetchVisualizationData() {
    const response = await fetch('/api/visualization', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ banner_type: bannerType, current_pity: currentPity }),
    });

    if (!response.ok) throw new Error('Failed to fetch visualization data');
    return await response.json();
  }

  function createCharts(data: any) {
    const totalPulls = currentPity + plannedPulls;
    const maxProbIndex = data.probability_per_roll.indexOf(
      Math.max(...data.probability_per_roll)
    );
    const maxProbRoll = data.rolls[maxProbIndex];

    // Cumulative Chart (now first)
    cumulativeChart = new Chart(cumulativeChartCanvas, {
      type: 'line',
      data: {
        labels: data.rolls,
        datasets: [{
          label: 'Cumulative Probability',
          data: data.cumulative_probability.map((p: number) => p * 100),
          borderColor: 'rgb(220, 57, 18)',
          borderWidth: 2,
          tension: 0.4,
          fill: false,
          pointRadius: 0
        }]
      },
      options: {
        responsive: true,
        interaction: {
          intersect: false,
          mode: 'index'
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              font: { size: 10 },
              boxWidth: 15,
              padding: 10
            }
          },
          annotation: {
            annotations: {
              softPity: {
                type: 'line',
                xMin: data.soft_pity_start,
                xMax: data.soft_pity_start,
                borderColor: 'rgb(85, 168, 104)',
                borderWidth: 1.5,
                borderDash: [2, 2],
                label: {
                  content: `Soft Pity (${data.soft_pity_start})`,
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(85, 168, 104)',
                  font: { size: 11 },
                  padding: 4
                }
              },
              fiftyPercent: {
                type: 'line',
                yMin: 50,
                yMax: 50,
                borderColor: 'rgb(51, 102, 204)',
                borderWidth: 1.5,
                borderDash: [2, 2],
                label: {
                  content: '50% Chance',
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(51, 102, 204)',
                  font: { size: 11 },
                  padding: 4
                }
              },
              guarantee: {
                type: 'line',
                yMin: 100,
                yMax: 100,
                borderColor: 'rgb(46, 184, 92)',
                borderWidth: 1.5,
                borderDash: [4, 4],
                label: {
                  content: '100% Guarantee',
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(46, 184, 92)',
                  font: { size: 11 },
                  padding: 4
                }
              },
              hardPity: {
                type: 'line',
                xMin: data.hard_pity,
                xMax: data.hard_pity,
                borderColor: 'rgb(255, 127, 80)',
                borderWidth: 1.5,
                borderDash: [6, 6],
                label: {
                  content: `Hard Pity (${data.hard_pity})`,
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(255, 127, 80)',
                  font: { size: 11 },
                  padding: 4
                }
              },
              currentTotal: {
                type: 'line',
                xMin: totalPulls,
                xMax: totalPulls,
                borderColor: 'rgb(255, 0, 0)',
                borderWidth: 2,
                label: {
                  content: `Current Total (${totalPulls})`,
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(255, 0, 0)',
                  font: { size: 11 },
                  padding: 4
                }
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            border: {
              display: true,
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Roll Number'
            }
          },
          y: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Cumulative Probability (%)'
            },
            min: 0,
            max: 100,
            ticks: {
              callback: (value) => (value as number).toFixed(0)
            }
          }
        }
      }
    });

    // Distribution Chart
    distributionChart = new Chart(distributionChartCanvas, {
      type: 'line',
      data: {
        labels: data.rolls,
        datasets: [{
          label: 'Probability per Roll',
          data: data.probability_per_roll.map((p: number) => p * 100),
          borderColor: 'rgb(76, 114, 176)',
          borderWidth: 2,
          tension: 0.4,
          fill: false,
          pointRadius: 0
        }]
      },
      options: {
        responsive: true,
        interaction: {
          intersect: false,
          mode: 'index'
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              font: { size: 10 },
              boxWidth: 15,
              padding: 10
            }
          },
          annotation: {
            annotations: {
              mostLikelyRoll: {
                type: 'line',
                xMin: maxProbRoll,
                xMax: maxProbRoll,
                borderColor: 'rgb(196, 78, 82)',
                borderWidth: 1.5,
                borderDash: [6, 6],
                label: {
                  content: `Most Likely Roll (${maxProbRoll})`,
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(196, 78, 82)',
                  font: { size: 11 },
                  padding: 4
                }
              },
              softPity: {
                type: 'line',
                xMin: data.soft_pity_start,
                xMax: data.soft_pity_start,
                borderColor: 'rgb(85, 168, 104)',
                borderWidth: 1.5,
                borderDash: [2, 2],
                label: {
                  content: `Soft Pity (${data.soft_pity_start})`,
                  display: true,
                  position: 'end',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(85, 168, 104)',
                  font: { size: 11 },
                  padding: 4
                }
              },
              currentTotal: {
                type: 'line',
                xMin: totalPulls,
                xMax: totalPulls,
                borderColor: 'rgb(255, 0, 0)',
                borderWidth: 2,
                label: {
                  content: `Current Total (${totalPulls})`,
                  display: true,
                  position: 'start',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  color: 'rgb(255, 0, 0)',
                  font: { size: 11 },
                  padding: 4
                }
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            border: {
              display: true,
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Roll Number'
            },
            ticks: {
              font: { size: 11 }
            }
          },
          y: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Probability per Roll (%)',
              font: { size: 12 },
              padding: { bottom: 10 }
            },
            ticks: {
              font: { size: 11 },
              callback: (value) => (value as number).toFixed(2)
            }
          }
        }
      }
    });
  }

  async function updateCharts() {
    if (!distributionChartCanvas || !cumulativeChartCanvas) return;
    
    if (distributionChart) distributionChart.destroy();
    if (cumulativeChart) cumulativeChart.destroy();
    
    const data = await fetchVisualizationData();
    createCharts(data);
  }

  $: {
    if (result && distributionChartCanvas && cumulativeChartCanvas) {
      updateCharts();
    }
  }
</script>

<div class="chart-container">
  <div class="chart-wrapper">
    <h3 class="chart-title">
      Cumulative Probability
    </h3>
    <div class="chart-canvas-container">
      <canvas bind:this={cumulativeChartCanvas}></canvas>
    </div>
  </div>

  <div class="chart-wrapper">
    <h3 class="chart-title">
      Successful Pull Distribution
    </h3>
    <div class="chart-canvas-container">
      <canvas bind:this={distributionChartCanvas}></canvas>
    </div>
  </div>
</div>