<script lang="ts">
  import {
    Chart,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    LineController,
    Title,
    Tooltip,
    Legend,
    type ChartConfiguration,
    type InteractionModeMap
  } from 'chart.js';
  import annotationPlugin from 'chartjs-plugin-annotation';

  // Register required components
  Chart.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    LineController,
    Title,
    Tooltip,
    Legend,
    annotationPlugin
  );
  
  export let bannerType: string;
  export let currentPity: number;
  export let plannedPulls: number;
  export let result: any;
  
  let cumulativeChartCanvas: HTMLCanvasElement;
  let distributionChartCanvas: HTMLCanvasElement;
  let cumulativeChart: Chart | null = null;
  let distributionChart: Chart | null = null;

  async function fetchVisualizationData() {
    try {
      console.log('Fetching visualization data for:', bannerType, 'current pity:', currentPity);
      const response = await fetch('/api/visualization', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          banner_type: bannerType, 
          current_pity: currentPity 
        })
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const text = await response.text();
        console.error('API Error Response:', {
          status: response.status,
          statusText: response.statusText,
          body: text
        });
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Visualization data received:', data);
      return data;
    } catch (error) {
      console.error('Visualization API error:', error);
      throw error;
    }
  }

  function createCharts(data: any) {
    const totalPulls = currentPity + plannedPulls;
    const maxProbIndex = data.probability_per_roll.indexOf(
      Math.max(...data.probability_per_roll)
    );
    const maxProbRoll = data.rolls[maxProbIndex];

    const commonScaleOptions = {
      x: {
        type: 'linear' as const,
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
      }
    };

    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index' as keyof InteractionModeMap
      }
    };

    // Cumulative Chart configuration
    const cumulativeConfig: ChartConfiguration<'line'> = {
      type: 'line',
      data: {
        labels: data.rolls,
        datasets: [{
          label: 'Cumulative Probability',
          data: data.cumulative_probability.map((p: number, i: number) => ({
            x: data.rolls[i],
            y: p * 100
          })),
          borderColor: 'rgb(220, 57, 18)',
          borderWidth: 2,
          tension: 0.4,
          fill: false,
          pointRadius: 0
        }]
      },
      options: {
        ...commonOptions,
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
                  yAdjust: -160,
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
                  yAdjust: -30,
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
          ...commonScaleOptions,
          y: {
            type: 'linear' as const,
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
              callback: function(tickValue: number | string): string {
                return typeof tickValue === 'number' ? tickValue.toFixed(2) : tickValue;
              }
            }
          }
        }
      }
    };

    // Distribution Chart configuration
    const distributionConfig: ChartConfiguration<'line'> = {
      type: 'line',
      data: {
        labels: data.rolls,
        datasets: [{
          label: 'Probability per Roll',
          data: data.probability_per_roll.map((p: number, i: number) => ({
            x: data.rolls[i],
            y: p * 100
          })),
          borderColor: 'rgb(76, 114, 176)',
          borderWidth: 2,
          tension: 0.4,
          fill: false,
          pointRadius: 0
        }]
      },
      options: {
        ...commonOptions,
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
                  position: 'start',
                  yAdjust: -160,
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
                  yAdjust: -30,
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
          ...commonScaleOptions,
          y: {
            type: 'linear' as const,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Probability per Roll (%)'
            },
            ticks: {
              callback: function(tickValue: number | string): string {
                return typeof tickValue === 'number' ? tickValue.toFixed(2) : tickValue;
              }
            }
          }
        }
      }
    };

    // Create new charts
    cumulativeChart = new Chart(cumulativeChartCanvas, cumulativeConfig);
    distributionChart = new Chart(distributionChartCanvas, distributionConfig);
  }

  async function updateCharts() {
    if (!distributionChartCanvas || !cumulativeChartCanvas) return;
    
    // Destroy existing charts
    if (distributionChart) {
      distributionChart.destroy();
      distributionChart = null;
    }
    if (cumulativeChart) {
      cumulativeChart.destroy();
      cumulativeChart = null;
    }
    
    try {
      const data = await fetchVisualizationData();
      createCharts(data);
    } catch (error) {
      console.error('Failed to update charts:', error);
    }
  }

  $: {
    if (result && distributionChartCanvas && cumulativeChartCanvas) {
      console.log('Updating charts with new data');
      updateCharts().catch(error => {
        console.error('Failed to update charts:', error);
      });
    } else {
      console.log('Skipping chart update:', {
        hasResult: !!result,
        hasDistributionCanvas: !!distributionChartCanvas,
        hasCumulativeCanvas: !!cumulativeChartCanvas
      });
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